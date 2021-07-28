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

import figureo.serialize
import figureo.standard.converter
import figureo.utils


def work(
    path: str,
    pages: tuple = None,
) -> figureo.utils.DumpedFigureInformation:
    pages = sorted(pages) if pages else pages

    figures = figureo.standard.converter.extract_figures(path, pages=pages)

    dumped = figureo.serialize.dump_figures(figures)
    return dumped
