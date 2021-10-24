# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

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
)


class FigureConverter(rawmaker.converter.basic.FlippedLayoutAnalyzer):

    def __init__(self, boundings: list = None, tables: list = None):
        super().__init__(laparams=LAYOUT)
        self.boundings = boundings
        self.tables = tables
        self.content = []
        self.page = 0
        self.nonfigure = collections.defaultdict(list)
        self.caption = collections.defaultdict(list)

    def receive_layout(self, ltpage):
        super().receive_layout(ltpage)
        bounding = None
        tables = None
        if self.tables:
            tables = utila.select_content(self.tables, self.page)
        if self.boundings:
            bounding = utila.select_page(self.boundings, self.page)
        if bounding:
            pagesize = (0, bounding.top, ltpage.width, bounding.bottom)
        else:
            # white page or no self.boundings defined.
            pagesize = (0, 0, ltpage.width, ltpage.height)
        for item in ltpage:
            self.render_pagecontent(self.page, item, pagesize, tables=tables)

    def render_pagecontent(self, pageid, item, pagesize=None, tables=None):
        """Collect all figures."""
        # strip potential figure bounding
        item.bbox = figure_bounding(item)
        if imageonly(item):
            utila.debug('figure as image container')
            # handled by --images, refactor later
            return
        if not valid_area(item.bbox, pagesize, tables):
            # check after figure to avoid skipping figure
            return
        if iscaption(item):
            self.caption[pageid].append((item.bbox[1] + item.bbox[3]) / 2)
            return
        if too_long(item):
            return
        if isinstance(item, pdfminer.layout.LTRect) and not item.linewidth:
            # skip hidden Rectangle
            return
        if isinvalid(item):
            return
        self.nonfigure[pageid].append(item)

    def figures(self) -> iamraw.Figures:
        """Create `text` figures after extraction complete pages. This
        method is only runned once."""
        merged = merge_figures(self.nonfigure, breaker=self.caption)
        # TODO: RENDER INTO MERGED FIGURES
        self.nonfigure.clear()
        self.caption.clear()
        if merged:
            self.content.extend(merged)
        return self.content


def figure_bounding(figure):
    if not isinstance(figure, pdfminer.layout.LTFigure):
        return figure.bbox
    boundings = [item.bbox for item in figure]
    result = utila.rectangle_max(boundings)
    return result


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
    tables: iamraw.TableBoundings = None,
    borderwidth=128,
) -> bool:
    tables = tables if tables else []
    # borderwidth: minus means a little bit outside of the page. This often
    # happens when having full page images.
    # borderwidth: increase borderwidth to handle bad pdf printing
    inside = (
        pagesize[0] - borderwidth,
        pagesize[1],
        pagesize[2] + borderwidth,
        pagesize[3],
    )
    for table in tables:
        # does element collide with table bounding
        if utila.intersecting_rectangle(table.bounding, bbox):
            return False
    if utila.intersecting_rectangle(inside, bbox):
        # intersecting with content border
        return True
    return False


def leftupper_dot(raw, unique: int):
    # The figure name is determined due hashing the figure content. If
    # both figures are equal(empty and same size for example) the figures
    # have the same name and one image information is lost. Therefore we
    # include the pageid id into a central pixel in the middle of the
    # figure. As a result of this, we do not lose bounding information.
    renderer = PIL.ImageDraw.Draw(raw, mode='RGBA')
    renderer.point([0, 0, 1, 1], fill=(255, 255, 255, unique))


def merge_figures(pagefigures, breaker) -> iamraw.Figures:
    """Group parts of figures, convert and export as raw image file."""
    result = []
    for page, values in pagefigures.items():
        figures = figureo.standard.text.text_figures(
            values,
            breaker=breaker[page],
        )
        for index, figure in enumerate(figures):
            figure.index = index
            figure.page = page
            leftupper_dot(figure.data, unique=page)
        result.extend(figures)
    return result


def extract_figures(
    document: str,
    boundings: list = None,
    tables: list = None,
    pages: tuple = None,
) -> iamraw.Figures:
    with rawmaker.reader.read(document) as pdf:
        # Processing layout
        content = pdfminer.pdfpage.PDFPage.create_pages(pdf)
        device = FigureConverter(boundings=boundings, tables=tables)
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
    figures = device.figures()
    return figures


def extract_figure(figure, pageid: int = None) -> iamraw.Figure:
    content = figure._objs  #  pylint:disable=W0212
    if len(content) == 1 and isinstance(content[0], pdfminer.layout.LTImage):
        # TODO: CHECK THIS
        # no figure, just an image container
        return None
    bounding = (figure.x0, figure.y0, figure.x1, figure.y1)
    try:
        # TODO: USE NEW PROCES?
        raw = figureo.utils.rawfigure_frombounding(bounding)
    except MemoryError:
        utila.error(f'could not render figure on page {pageid}: {bounding}')
        return None
    result = iamraw.Figure(data=raw, bounding=bounding)
    return result
