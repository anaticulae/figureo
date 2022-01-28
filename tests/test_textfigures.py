# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pdfminer.layout import LTLine
from pdfminer.layout import LTRect

import figureo.standard.text

EXAMPLE = [
    LTLine(linewidth=1, p0=(81.170, 55.530), p1=(297.640, 55.530)),
    LTLine(linewidth=1, p0=(297.640, 55.530), p1=(514.100, 55.530)),
    LTRect(linewidth=1, bbox=(85.860, 267.130, 110.760, 292.040)),
    LTRect(linewidth=1, bbox=(112.260, 267.130, 180.000, 292.040)),
    LTRect(linewidth=1, bbox=(181.500, 267.130, 206.410, 292.040)),
    LTRect(linewidth=1, bbox=(207.800, 267.130, 232.710, 292.040)),
    LTRect(linewidth=1, bbox=(234.100, 267.130, 259.010, 292.040)),
    LTRect(linewidth=1, bbox=(260.500, 267.130, 304.340, 292.040)),
    LTRect(linewidth=1, bbox=(307.130, 267.130, 374.870, 292.040)),
    LTRect(linewidth=1, bbox=(376.470, 267.130, 444.220, 292.040)),
    LTRect(linewidth=1, bbox=(445.810, 267.130, 477.690, 292.040)),
    LTRect(linewidth=1, bbox=(479.290, 267.130, 511.170, 292.040)),
    LTLine(linewidth=1, p0=(81.170, 622.350), p1=(254.340, 622.350)),
]


def test_create_textfigures():
    result = figureo.standard.text.text_figures(
        EXAMPLE,
        width_min=50,
        height_min=50,
        area_min=50 * 50,
    )
    assert len(result) == 1
