# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import io
import typing

import PIL.Image
import utila

DumpedFigureInformation = typing.List[typing.Tuple[str, bytes]]


def image_tobytes(image) -> bytes:
    raw = io.BytesIO()
    image.save(raw, format='PNG')
    raw.seek(0)
    result = raw.getvalue()
    return result


WHITE = 1
RGBA = 'RGBA'

IMAGE_WIDTH_MAX = 1024
IMAGE_HEIGHT_MAX = 768


def rawfigure_frombounding(bbox, mode=RGBA, background=WHITE) -> PIL.Image:
    width = utila.rectangle_width(bbox)
    height = utila.rectangle_height(bbox)
    # limit max figure size to avoid too much memory consumption
    width = utila.mins(width, IMAGE_WIDTH_MAX)
    height = utila.mins(height, IMAGE_HEIGHT_MAX)
    # ensure positive figure size
    if width < 0 or height < 0:
        utila.error(f'negative figure size: {width} {height}')
    width = utila.maxs(width, 1)
    height = utila.maxs(height, 1)
    # figure image size
    size = (int(width), int(height))
    raw = PIL.Image.new(mode, size, color=background)
    return raw
