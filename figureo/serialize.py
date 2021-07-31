# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila

import figureo.utils


def dump_figures(figures) -> figureo.utils.DumpedFigureInformation:
    result = []
    for figure in figures:
        bounding = tuple(figure.bounding)
        width = figure.bounding[2] - figure.bounding[0]
        height = figure.bounding[3] - figure.bounding[1]
        width, height = utila.roundme(width, height)
        info = iamraw.ImageInformation(
            page=figure.page,
            width=width,
            height=height,
            bounding=bounding,
        )
        info = serializeraw.dump_image_info(info)
        result.append((info, figure.data))
    return result
