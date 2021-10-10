# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pdfminer.layout
import utila

import figureo.utils

# TODO: REMOVE HORIZONTAL AND VERTICAL LINES TO AVOID DETECTING TABLES AS
# FIGURE?

TEXT_ONLY = (
    pdfminer.layout.LTTextBoxHorizontal,
    pdfminer.layout.LTTextBoxVertical,
)


def text_figures(
    items,
    width_min=150,
    height_min=100,
    area_min=150 * 150,
    breaker=None,
) -> iamraw.Figure:
    alltext = all((isinstance(item, TEXT_ONLY) for item in items))
    if alltext:
        # do not detect figures which consist out of text elements. The
        # false positive rate is too high.
        return []

    def valid(bounding: tuple) -> bool:
        """Ensure that text figure is big enougth to avoid many false
        positive renderings."""
        if not textonly(bounding, items):
            return True
        if utila.rectangle_size(bounding) < area_min:
            return False
        if utila.rectangle_width(bounding) >= width_min:
            return True
        if utila.rectangle_height(bounding) >= height_min:
            return True
        return False

    result = []
    for group in splitby_breaker(items, breaker):
        clustered = cluster(group)
        for bounding in clustered:
            raw = figureo.utils.rawfigure_frombounding(bounding)
            figure = iamraw.Figure(data=raw, bounding=bounding)
            result.append(figure)

    # remove too small figures, disable for cluster which contains
    # rectangle, lines, curve etc. and accept them all.
    result = [item for item in result if valid(item.bounding)]
    return result


def splitby_breaker(items, breaker):
    if not breaker:
        return [items]
    breaker = sorted(breaker)
    grouped = utila.Buckets(border=breaker)
    grouped.selector = lambda x: (x.bbox[1] + x.bbox[3]) / 2
    for item in items:
        grouped.add(item)
    result = list(grouped)
    return result


def textonly(bounding, items: list) -> bool:
    # TODO: VERIFY THIS
    notext = [
        item for item in items
        if not isinstance(item, pdfminer.layout.LTTextBoxHorizontal)
    ]
    for item in notext:
        if utila.rectangle_inside(bounding, item.bbox, diff=10):
            return False
    return True


MIN_CLUSTER_SIZE = 25


def cluster(  # pylint:disable=R0914
        items: list,
        min_cluster_size=MIN_CLUSTER_SIZE,
):
    bucket = utila.Buckets(utila.ranges(0, 1000, 15), sorting=True)
    for item in items:
        start, end = item.bbox[1], item.bbox[3]
        # left to right to ensure that line is marked more than one
        # keep y-expansion in calculation
        # for _ in utila.ranges(item.bbox[0], item.bbox[2], step=50):
        for coordinate in utila.ranges(start, end, step=5):
            bucket.add(utila.roundme(coordinate))
    # select areas with enough items
    content = list(bucket)  # TODO: REMOVE after upgrading UTILA
    content = utila.groupby_neighbors(content)
    # TODO: CHECK MIN_CLUSTER_SIZE CAUSE SET REMOVES ITEMS OUT OF CONTENT
    selected = [set(item) for item in content if len(item) >= min_cluster_size]
    # prepare result
    result = []
    for current in selected:
        y0 = min(current)
        y1 = max(current)
        incluster = [
            item.bbox
            for item in items
            if y0 <= item.bbox[1] <= y1 or y0 <= item.bbox[3] <= y1
        ]
        x0 = min(item[0] for item in incluster)
        x1 = max(item[2] for item in incluster)
        bounding = (x0, y0, x1, y1)
        result.append(bounding)
    return result
