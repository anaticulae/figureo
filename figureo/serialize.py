# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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
        width = utila.rectangle_width(figure.bounding)
        height = utila.rectangle_height(figure.bounding)
        info = iamraw.ImageInformation(
            page=figure.page,
            width=width,
            height=height,
            bounding=bounding,
            figure=True,
        )
        info = serializeraw.dump_image_info(info)
        result.append((info, figure.data))
    return result
