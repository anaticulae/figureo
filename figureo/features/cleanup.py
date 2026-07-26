# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utilo


def work(
    standard: str,  # pylint:disable=W0613
    *sources: list,
    pages: tuple = None,
) -> list[tuple[str, str]]:
    """\
    ::: require standard to run standard before cleanup
    """
    sources = setup_sources(sources)
    # load data
    figures, images = prepare(sources, pages=pages)
    result = hide(figures, images)
    # update hidden flag
    dumped = [
        (path, serializeraw.dump_image_info(image)) for image, path in result
    ]
    return dumped


def setup_sources(sources) -> list:
    # separate steps are required, cause standard produces figure files
    # which are required for cleanup step. In the current state utilo
    # determines inputs only at startup time. Therefore figureo wont know
    # than theses later generated files exists. TODO: REMOVE AFTER
    # UPGRADING INPUTS AFTER EVERY STEP
    # skip -i pdf source file
    # TODO: REMOVE AFTER UPGRADING UTILA
    sources = [item for item in sources if utilo.file_ext(item) == 'yaml']
    directory = set(utilo.path_parent(item) for item in sources)
    for path in directory:
        sources.extend(utilo.file_list(path, include='yaml', absolute=True))
    sources = [utilo.forward_slash(item) for item in sources]
    sources = utilo.unique(sources)
    return sources


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
                if not utilo.rect_intersecting(
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
    content = utilo.flatten_content(loaded)
    # divide figures and images
    images, figures = utilo.partition(lambda x: x[0].dpi, content)
    # group figure by page value
    figures_grouped = utilo.groupby_x(figures, selector=lambda x: x[0].page)
    figures_grouped: dict = {item[0][0].page: item for item in figures_grouped}
    return figures_grouped, images
