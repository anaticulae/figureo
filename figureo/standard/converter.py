# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import contextlib

import configo
import elements
import iamraw
import pdfminer
import pdfminer.layout
import PIL.ImageDraw
import rawmaker.converter.basic
import rawmaker.reader
import utila

import figureo.standard.text
import figureo.utils

# use layout to group test to avoid handling to much LTChar-data.
LAYOUT = pdfminer.layout.LAParams(
    char_margin=2.7,
    line_margin=0.01,
    # improve equal line merge: see diss205p141
    # Example: Radius beträgt √ Wert der Zielfunktion
    line_overlap=0.0,
)


class FigureConverter(rawmaker.converter.basic.FlippedLayoutAnalyzer):

    def __init__(self, boundings: list = None, nofigures: list = None):
        super().__init__(laparams=LAYOUT)
        self.boundings = boundings
        self.nofigures = nofigures  # TODO: VERIFY NAMING
        self.content = []
        self.page = 0
        self.nonfigure = collections.defaultdict(list)
        self.invalids = collections.defaultdict(list)
        self.caption = collections.defaultdict(list)
        self.images = collections.defaultdict(list)

    def receive_layout(self, ltpage):
        super().receive_layout(ltpage)
        bounding = None
        nofigures = None
        if self.nofigures:
            nofigures = utila.select_content(self.nofigures, self.page)
        if self.boundings:
            bounding = utila.select_page(self.boundings, self.page)
        pagesize = determine_pagesize(bounding, ltpage)
        for item in ltpage:
            self.render_pagecontent(
                item,
                self.page,
                pagesize,
                nofigures=nofigures,
            )

    def render_pagecontent(self, item, pageid, pagesize=None, nofigures=None):  # pylint:disable=R0911
        """Collect all figures."""
        # strip potential figure bounding
        item.bbox = figure_bounding(item)
        if not item.bbox:
            # skip invisible item
            self.invalids[pageid].append(item)
            return
        if imageonly(item):
            utila.debug(f'figure as image container: {pageid}')
            self.images[pageid].append(item)
            # handled by --images, refactor later
            return
        if not valid_area(item.bbox, pagesize, nofigures):
            # check after figure to avoid skipping figure
            return
        if iscaption(item):
            self.caption[pageid].append((item.bbox[1] + item.bbox[3]) / 2)
            return
        if too_long(item):
            self.invalids[pageid].append(item)
            return
        if isrectangle_hidden(item):
            # skip hidden Rectangle
            return
        if isinvalid(item):
            return
        self.nonfigure[pageid].append(item)

    def figures(self) -> iamraw.Figures:
        """Create `text` figures after extraction complete pages. This
        method is only runned once."""
        merged = merge_figures(
            pagefigures=self.nonfigure,
            invalids=self.invalids,
            breaker=self.caption,
            images=self.images,
        )
        # TODO: RENDER INTO MERGED FIGURES
        self.nonfigure.clear()
        self.invalids.clear()
        self.caption.clear()
        self.images.clear()
        if merged:
            self.content.extend(merged)
        return self.content


def determine_pagesize(bounding, ltpage):
    if not bounding:
        # white page or no self.boundings defined.
        pagesize = (0, 0, ltpage.width, ltpage.height)
        return pagesize
    normal = ltpage.height > ltpage.width
    if normal:
        # normal
        pagesize = (0, bounding.top, ltpage.width, bounding.bottom)
        return pagesize
    # rotated
    pagesize = (
        ltpage.width - bounding.bottom,
        0,
        ltpage.width - bounding.top,
        ltpage.height,
    )
    return pagesize


def isrectangle_hidden(item) -> bool:
    if not isinstance(item, pdfminer.layout.LTRect):
        return False
    if 0.0 < item.width < 1.0 and item.height:
        # rectangle is a vertical line
        return False
    if 0.0 < item.height < 1.0 and item.width:
        # rectangle is a horizontal line
        return False
    if item.linewidth:
        return False
    return True


def figure_bounding(figure) -> tuple:
    if not isinstance(figure, pdfminer.layout.LTFigure):
        return figure.bbox
    figure = [item for item in figure if visible(item)]
    boundings = []
    for item in figure:
        if isinstance(item, pdfminer.layout.LTFigure):
            # figure inside a figure
            bounding = figure_bounding(item)
        else:
            bounding = item.bbox
        if not bounding:
            # invisible bounding
            continue
        boundings.append(bounding)
    if not boundings:
        # invisible item
        return None
    result = utila.rectangle_max(boundings)
    return result


def visible(item) -> bool:
    with contextlib.suppress(AttributeError):
        # TODO: INVESTIGATE THIS
        if item.linewidth:
            return True
        if item.fill:
            if not item.evenodd:
                return True
            return False
        if not item.stroking_color and not item.non_stroking_color:
            return False
    return True


def isinvalid(item) -> bool:
    if not isinstance(item, pdfminer.layout.LTTextBoxHorizontal):
        return False
    # TODO: REMOVE STRIP LATER
    text = item.get_text().strip()
    if not text:
        return True
    if text == '.':
        return True
    if text.count('(') != text.count(')'):
        return True
    if contains_listof(text):
        return True
    return False


def contains_listof(raw: str) -> bool:
    dots_with_spaces = raw.count('. . .')
    connected_dots = raw.count('....')
    if dots_with_spaces:
        return True
    if connected_dots:
        return True
    return False


def iscaption(item) -> bool:
    if not isinstance(item, pdfminer.layout.LTTextBoxHorizontal):
        return False
    if elements.iscaption(item.get_text()):
        return True
    return False


def imageonly(figure) -> bool:
    if not isinstance(figure, pdfminer.layout.LTFigure):
        return False
    images = figure._objs  # pylint:disable=W0212
    if len(images) != 1:
        return False
    if isinstance(images[0], pdfminer.layout.LTImage):
        return True
    if isinstance(images[0], pdfminer.layout.LTFigure):
        if len(images[0]._objs) == 1:  # pylint:disable=W0212
            return True
    return False


FIGURE_TEXT_LENGTH_MAX = configo.HV_INT_PLUS(default=20)


def too_long(item) -> bool:
    if not isinstance(item, pdfminer.layout.LTTextBoxHorizontal):
        return False
    # skip content lines
    text = item.get_text().strip()
    if not text:
        return False
    if item.x0 > 200 and item.x1 < 450:
        # do not ignore centered text
        return False
    maxs = utila.maxs([len(item) for item in text.splitlines()])
    if maxs > FIGURE_TEXT_LENGTH_MAX:
        return True
    return False


def valid_area(
    bbox: utila.Rectangle,
    pagesize: tuple,
    nofigures: iamraw.TableBoundings = None,
    borderwidth=128,
) -> bool:
    nofigures = nofigures if nofigures else []
    # borderwidth: minus means a little bit outside of the page. This often
    # happens when having full page images.
    # borderwidth: increase borderwidth to handle bad pdf printing
    inside = (
        pagesize[0] - borderwidth,
        pagesize[1],
        pagesize[2] + borderwidth,
        pagesize[3],
    )
    for noarea in nofigures:
        # does element collide with table bounding
        if utila.intersecting_rectangle(bounding_area(noarea), bbox):
            return False
    if utila.intersecting_rectangle(inside, bbox):
        # intersecting with content border
        return True
    return False


def bounding_area(item) -> tuple:
    with contextlib.suppress(AttributeError):
        return item.bounding
    with contextlib.suppress(AttributeError):
        return item.bbox
    return item


def leftupper_dot(raw, unique: int):
    # The figure name is determined due hashing the figure content. If
    # both figures are equal(empty and same size for example) the figures
    # have the same name and one image information is lost. Therefore we
    # include the pageid id into a central pixel in the middle of the
    # figure. As a result of this, we do not lose bounding information.
    renderer = PIL.ImageDraw.Draw(raw, mode='RGBA')
    renderer.point([0, 0, 1, 1], fill=(255, 255, 255, unique))


def merge_figures(pagefigures, invalids, breaker, images) -> iamraw.Figures:
    """Group parts of figures, convert and export as raw image file."""
    result = []
    for page, values in pagefigures.items():
        figures = figureo.standard.text.text_figures(
            values,
            invalids=invalids[page],
            breaker=breaker[page],
        )
        figures = merge_images_into_textfigures(figures, images[page])
        for index, figure in enumerate(figures):
            figure.index = index
            figure.page = page
            if figure.data is None:
                figure.data = figureo.utils.rawfigure_frombounding(
                    figure.bounding)
            leftupper_dot(figure.data, unique=page)
        result.extend(figures)
    return result


def merge_images_into_textfigures(figures: list, images: list) -> list:
    """Merge images which intersects with text figure-bounding into
    text-figure.

    Image-Only figures are not handled by textfigure-detector, therefore
    we have to merge them if there are part of figure.
    """
    if not images:
        return figures
    for figure in figures:
        for image in images:
            # TODO: DO NOT MERGE TWICE?
            if not utila.intersecting_rectangle(
                    figure.bounding,
                    image.bbox,
            ):
                continue
            # update figure bounding
            figure.bounding = utila.rectangle_max((
                figure.bounding,
                image.bbox,
            ))
    return figures


def extract_figures(
    document: str,
    boundings: list = None,
    nofigures: list = None,
    pages: tuple = None,
) -> iamraw.Figures:
    with rawmaker.reader.read(document) as pdf:
        # Processing layout
        content = pdfminer.pdfpage.PDFPage.create_pages(pdf)
        device = FigureConverter(boundings=boundings, nofigures=nofigures)
        interpreter = pdfminer.pdfinterp.PDFPageInterpreter(
            device.resources,
            device,
        )
        with utila.SkipCollector(pages) as collector:
            for number, page in enumerate(content):
                if collector.skip(number):
                    continue
                device.page = number
                interpreter.process_page(page)
    result = device.figures()
    return result
