# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import pdfminer.layout
import utila

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
    invalids=None,
    breaker=None,
) -> iamraw.Figure:
    alltext = all((isinstance(item, TEXT_ONLY) for item in items))
    if alltext:
        # do not detect figures which consist out of text elements. The
        # false positive rate is too high.
        return []
    result = []
    for group in splitby_breaker(items, breaker):
        clustered = determine_clusters(group)
        for bounding in clustered:
            if not content_valid(bounding, content=items, invalids=invalids):
                continue
            figure = iamraw.Figure(bounding=bounding)
            result.append(figure)
    # remove too small figures, disable for cluster which contains
    # rectangle, lines, curve etc. and accept them all.
    result = [
        item for item in result
        if bounding_valid(item.bounding, items, width_min, height_min, area_min)
    ]
    second_look = figures_missing(items, result)
    if second_look:
        result.extend(second_look)
    return result


def figures_missing(items, done) -> list:
    """Backup strategy to detect all LTFigures which are not part of
    extracted text figures."""
    done = [item.bounding for item in done]
    figures = utila.select_type(items, selector=pdfminer.layout.LTFigure)
    result = []
    for item in figures:
        if utila.rectangles_intersecting(done, item.bbox):
            # LTFigure is already part of a text figure
            continue
        matching = [
            test.bbox
            for test in items
            if utila.intersecting_rectangle(item.bbox, test.bbox)
        ]
        bounding = utila.rectangle_max([item.bbox] + matching)
        figure = iamraw.Figure(bounding=bounding)
        result.append(figure)
    return result


def bounding_valid(bounding: tuple, items, width_min, height_min, area_min) -> bool:  # yapf:disable
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


CONTENT_INVALID_RATE_MAX = configo.HolyTable(items=[
    (5, 0.1),
    (10, 0.2),
    (15, 0.2),
    (20, 0.2),
    (30, 0.18),
    (40, 0.15),
])


def content_valid(bounding, content, invalids) -> bool:
    if not invalids:
        return True
    content = [
        item for item in content
        if utila.intersecting_rectangle(bounding, item.bbox)
    ]
    invalids = [
        item for item in invalids
        if utila.intersecting_rectangle(bounding, item.bbox)
    ]
    rate = len(invalids) / len(content)
    if rate > CONTENT_INVALID_RATE_MAX(len(content)):
        # too many invalid items
        return False
    return True


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


CLUSTER_SIZE_MIN = configo.HV_INT_PLUS(default=25)


def determine_clusters(
    items: list,
    cluster_size_min=CLUSTER_SIZE_MIN,
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
    content = utila.groupby_neighbors(bucket)
    # TODO: CHECK CLUSTER_SIZE_MIN CAUSE SET REMOVES ITEMS OUT OF CONTENT
    selected = [set(item) for item in content if len(item) >= cluster_size_min]
    # prepare result
    result = []
    for cluster in selected:
        bounding = determine_cluster_rectangle(cluster, items)
        result.append(bounding)
    return result


# A normal line of text is between 10-13 height
AREA_START_HEIGHT_MAX = configo.HV_FLOAT_PLUS(default=25.0)
# Covering less than this is detected as text line start
AREA_COVERING_RATE_MIN = configo.HV_PERCENT_PLUS(default=35.0)


def determine_cluster_rectangle(
    cluster,
    items,
    first=AREA_START_HEIGHT_MAX,
    # area_covering_min=AREA_COVERING_RATE_MIN,
):
    y0 = min(cluster)
    y1 = max(cluster)
    incluster = [
        item for item in items
        if y0 <= item.bbox[1] <= y1 or y0 <= item.bbox[3] <= y1
    ]
    x0 = min(item.bbox[0] for item in incluster)
    x1 = max(item.bbox[2] for item in incluster)
    # Does first line of text is included into text figure?
    # determine text start
    start_area = (x0, y0, x1, y0 + first)
    firstline = [
        item for item in items if utila.rectangle_inside(start_area, item.bbox)
    ]
    textline_in_figure = hanging_textline(start_area, firstline)
    if textline_in_figure:
        # remove line start if line start is detected
        for item in firstline:
            incluster.remove(item)
    # determine figure bounding
    result = utila.rectangle_max([item.bbox for item in incluster])
    return result


def hanging_textline(area, firstline) -> bool:
    buckets = utila.Buckets(border=utila.ranges(
        start=area[0],
        stop=area[2],
        step=20.0,
    ))
    for item in firstline:
        for x in utila.ranges(start=item.bbox[0], stop=item.bbox[2], step=5.0):
            buckets.add(x)
    # 1/3 2/3
    start, rest = splitby_percent(buckets, percent=0.35)
    if rateme(rest):
        return False
    if rateme(start) < 0.8:
        return True
    return False


def splitby_percent(items, percent=0.28):
    assert 1.0 >= percent >= 0.0
    splitindex = int(len(items) * percent)
    return items[0:splitindex], items[splitindex:]


def rateme(buckets) -> float:
    if not buckets:
        # TODO: ZERO OR ONE?
        return 0.0
    full = len([item for item in buckets if item])
    rate = full / len(buckets)
    return rate
