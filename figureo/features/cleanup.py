# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import serializeraw
import utila


def work(
    standard: str,  # pylint:disable=W0613
    *sources: list,
    pages: tuple = None,
) -> typing.List[typing.Tuple[str, str]]:
    """\
    ::: require standard to run standard before cleanup
    """
    # skip -i pdf source file
    # TODO: REMOVE AFTER UPGRADING UTILA
    sources = [item for item in sources if utila.file_ext(item) == 'yaml']
    # load data
    figures, images = prepare(sources, pages=pages)
    result = hide(figures, images)
    # update hidden flag
    dumped = [
        (path, serializeraw.dump_image_info(image)) for image, path in result
    ]
    return dumped


def hide(figures, images):
    result = []
    for page, figure in figures.items():
        for image in images:
            if image[0].page != page:
                # this image is not on the same page as the figure
                continue
            for fig in figure:
                # does the image intersects with the figure. Therefore we
                # want to hide this figure.
                if not utila.intersecting_rectangle(
                        fig[0].bounding,
                        image[0].bounding,
                ):
                    continue
                # disable image for further processing
                image[0].hidden = True
                result.append(image)
                break
    return result


def prepare(sources: list, pages: tuple = None) -> tuple:
    # load images
    loaded = serializeraw.load_image_infos_fromfiles(
        sources,
        path_append=True,
        pages=pages,
    )
    content = utila.flatten_content(loaded)
    # divide figures and images
    images, figures = utila.partition(lambda x: x[0].dpi, content)
    # group figure by page value
    figures_grouped = utila.groupby_x(figures, selector=lambda x: x[0].page)
    figures_grouped: dict = {item[0][0].page: item for item in figures_grouped}
    return figures_grouped, images
