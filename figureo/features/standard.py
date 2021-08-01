# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Figure Extractor

Extract figures and convert to images

"""

import ghost
import iamraw
import serializeraw
import utila

import figureo.serialize
import figureo.standard.converter
import figureo.utils


def work(
    path: str,
    content: str = None,
    tables: str = None,
    pages: tuple = None,
) -> figureo.utils.DumpedFigureInformation:
    pages = sorted(pages) if pages else pages
    if utila.exists(content):
        content = serializeraw.load_contentboundingbox(content, pages=pages)
    else:
        utila.debug(f'{content} does not exists')
        content = None
    if utila.exists(tables):
        tables = serializeraw.load_tables(tables, pages=pages)
    else:
        utila.debug(f'{tables} does not exists')
        tables = None
    figures = figureo.standard.converter.extract_figures(
        path,
        boundings=content,
        tables=tables,
        pages=pages,
    )
    if figures:
        figures = beautify_figures(figures, path)
    dumped = figureo.serialize.dump_figures(figures)
    return dumped


# 2 percent tolerance
SCALE = (0.99, 0.99, 1.01, 1.01)


def beautify_figures(figures, path: str):
    """Use ghost to render pdf and crop interested area."""
    boundings = [
        iamraw.ImageInformation(
            page=image.page,
            bounding=utila.rectangle_scale(image.bounding, SCALE),
        ) for image in figures
    ]
    extracted = ghost.images(path, boundings)
    for figure, image in zip(figures, extracted):
        figure.data = image
    return figures
