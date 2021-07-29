# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import math

import iamraw
import pdfminer
import pdfminer.layout
import PIL.Image
import PIL.ImageDraw
import rawmaker.converter.basic
import rawmaker.reader
import utila

import figureo.standard.text
import figureo.utils

# use layout to group test to avoid handling to much LTChar-data.
LAYOUT = pdfminer.layout.LAParams()


class FigureConverter(rawmaker.converter.basic.FlippedLayoutAnalyzer):

    def __init__(self, boundings: list = None):
        super().__init__(laparams=LAYOUT)
        self.boundings = boundings
        self.content = []
        self.page = 0
        self.nonfigure = collections.defaultdict(list)

    def receive_layout(self, ltpage):
        super().receive_layout(ltpage)
        if self.boundings:
            bounding = utila.select_page(self.boundings, self.page)
            pagesize = (0, bounding.top, ltpage.width, bounding.bottom)
        else:
            pagesize = (0, 0, ltpage.width, ltpage.height)
        for item in ltpage:
            self.render_pagecontent(self.page, item, pagesize)

    def render_pagecontent(self, pageid, item, pagesize=None):
        """Collect all figures."""
        if imageonly(item):
            utila.error('duplicated image')
            # return
            # handled by --images, refactor later
            # return
        if not valid_area(item.bbox, pagesize):
            # check after figure to avoid skipping figure
            return
        if too_long(item):
            return
        if isinstance(item, pdfminer.layout.LTRect) and item.linewidth == 0:
            # skip hidden Rectangle
            return

        self.nonfigure[pageid].append(item)

    def render_figure(self, item: pdfminer.layout.LTFigure, pageid: int):
        rendered = extract_figure(item, pageid)
        if rendered is None:
            return
        rendered.page = pageid
        self.content.append(rendered)

    def figures(self) -> iamraw.Figures:
        """Create `text` figures after extraction complete pages. This
        method is only runned once."""
        merged = merge_figures(self.nonfigure)
        # TODO: RENDER INTO MERGED FIGURES
        self.nonfigure.clear()
        if merged:
            self.content.extend(merged)
        return self.content


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
    if maxs > 10:
        return True
    return False


def valid_area(bbox: utila.Rectangle, pagesize: tuple, borderwidth=5) -> bool:
    # borderwith: minus means a little bit outside of the page. This often
    # happens when having full page images.
    inside = (
        pagesize[0] - borderwidth,
        pagesize[1] - borderwidth,
        pagesize[2] + borderwidth,
        pagesize[3] + borderwidth,
    )
    if utila.rectangle_inside(inside, bbox):
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


def merge_figures(pagefigures) -> iamraw.Figures:
    """Group parts of figures, convert and export as raw image file."""
    result = []
    for page, values in pagefigures.items():
        figures = figureo.standard.text.text_figures(values)
        for index, figure in enumerate(figures):
            figure.index = index
            figure.page = page
            leftupper_dot(figure.data, unique=page)
        result.extend(figures)
    return result


def extract_figures(
    document: str,
    boundings: list = None,
    pages: tuple = None,
) -> iamraw.Figures:
    with rawmaker.reader.read(document) as pdf:
        # Processing layout
        content = pdfminer.pdfpage.PDFPage.create_pages(pdf)
        device = FigureConverter(boundings=boundings)
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
    # TODO: Investigate about correct scaling.
    scalex, scaley = 4, 4
    # scalex, scaley = 1 / figure.matrix[0], 1 / figure.matrix[3]
    if scalex < 0 or scaley < 0:
        # TODO: DONT KNOW WHY THIS CAN HAPPEN?
        # TODO: INDICATE THIS FOR SOME USER DEFINED LAYOUT ERROR?
        utila.error(f'negative scaling: {scalex} {scaley}')
        scalex, scaley = math.fabs(scalex), math.fabs(scaley)

    bounding = scale_bounding(
        (figure.x0, figure.y0, figure.x1, figure.y1),
        (scalex, scaley),
    )

    offset = bounding[0], bounding[1]
    scale = scalex, scaley

    try:
        # TODO: USE NEW PROCES?
        raw = figureo.utils.rawfigure_frombounding(bounding)
    except MemoryError:
        utila.error(f'could not render figure on page {pageid}: {bounding}')
        return None
    renderer = PIL.ImageDraw.Draw(raw, mode='RGBA')

    for item in figure:
        render(item, offset, scale, renderer, raw)

    # scale bounding information to pdf size
    bounding = scale_bounding(bounding, (1.0 / scalex, 1.0 / scaley))

    result = iamraw.Figure(data=raw, bounding=bounding)
    return result


def render(item, offset, scale, renderer, rawbuffer):  # pylint:disable=R0914
    scalex, scaley = scale
    bounding = list(item.bbox)
    bounding[0] *= scale[0]
    bounding[2] *= scale[0]
    bounding[1] *= scale[1]
    bounding[3] *= scale[1]

    bounding[0] -= offset[0]
    bounding[2] -= offset[0]
    bounding[1] -= offset[1]
    bounding[3] -= offset[1]

    if isinstance(item, pdfminer.layout.LTLine):
        renderer.line(
            bounding,
            width=utila.maxs(int(item.linewidth), 1),
            fill='black',
        )
    elif isinstance(item, pdfminer.layout.LTRect):
        renderer.rectangle(
            bounding,
            width=utila.maxs(int(item.linewidth), 1),
            outline='black',
        )
    elif isinstance(item, pdfminer.layout.LTCurve):
        for current, after in zip(item.pts[0:-1], item.pts[1:]):
            expanded = pdfminer.layout.LTLine(
                linewidth=item.linewidth,
                p0=current,
                p1=after,
            )
            # TODO: 200 HACK FOR NOT FLIPPED COORDINATE
            render(expanded, (0, 200), (1.0, 1.0), renderer, rawbuffer)
    elif isinstance(item, pdfminer.layout.LTFigure):
        # render image
        images = item._objs[:]  # pylint:disable=W0212
        for image in images:
            render(image, offset, scale, renderer, rawbuffer)
    elif isinstance(item, pdfminer.layout.LTImage):
        raw = rawmaker.miner.images.image_fromlt(item)
        if not raw:
            utila.error('could not render `image_fromlt`')
            return
        size = (int(item.width * scalex), int(item.height * scaley))
        location = (int(item.x0 * scalex), int(item.y0 * scaley))
        resized = raw.resize(size, resample=PIL.Image.ANTIALIAS)
        rawbuffer.paste(resized, location)
    else:
        utila.error(f'not supported: could not render {item}')


def scale_bounding(bounding: tuple, scale: tuple) -> tuple:
    result = (
        bounding[0] * scale[0],
        bounding[1] * scale[1],
        bounding[2] * scale[0],
        bounding[3] * scale[1],
    )
    return result
