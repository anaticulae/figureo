# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw.images
import utilo
import utilotest

import tests


@pytest.mark.xfail(reason='new software')
@pytest.mark.timeout(60)
@pytest.mark.usefixtures('td')
@utilotest.nightly
@utilotest.requires(hoverpower.BACHELOR085_PDF)
def test_extract_figures_memory_error(mp, capsys):
    # TODO: VALIDATE THIS UNIT TEST. THE MEMORY ERROR LOOKS QUITE
    # CONFUSING, PAY ATENTION TO THE PAGE NUMBERS
    source = hoverpower.BACHELOR085_PDF
    tests.run(f'-i {source}  --standard --pages=75:', mp=mp)
    stderr = utilotest.stderr(capsys)
    assert 'could not render' in stderr, str(stderr)


@utilotest.requires(hoverpower.MASTER155_PDF)
def test_figure_master155_page15(td, mp):
    source = hoverpower.MASTER155_PDF
    tests.run(f'-i {source} --standard --pages=15', mp=mp)
    imageinformation = serializeraw.load_image_infos_frompath(
        td.tmpdir.join('rawmaker__images_images'))
    assert len(imageinformation) == 1


def test_figure_master155_page17(td, mp):
    """Include lower 0, 5, 10 base."""
    pdf = hoverpower.MASTER155_PDF
    images = tests.standard_figures(pdf, 17, td, mp)
    assert len(images) == 1
    bounding = images[0].bounding
    expected = (155.76, 182.04, 514.03, 389.72)
    assert utilo.nears(bounding, expected, diff=25.0)


@utilotest.requires(hoverpower.BACHELOR090_PDF)
@pytest.mark.usefixtures('td')
def test_bachelor90_whitepage_error(mp):
    """First page is a white page, this page produced an missing
    bounding error."""
    source = hoverpower.BACHELOR090_PDF
    pages = '0:10'
    tests.run(
        f'-i {source} -i {hoverpower.link(source)} --standard --pages={pages}',
        mp=mp,
    )


def test_bachelor90_text_ending_inside_figure(td, mp):
    source = hoverpower.BACHELOR090_PDF
    images = tests.standard_figures(source, 57, td, mp)
    assert len(images) == 1
    bounding = images[0].bounding
    expected = (112.83, 399.27, 479.46, 644.35)
    assert utilo.nears(bounding, expected)


@pytest.mark.xfail(reason='integrate new software')
@utilotest.requires(hoverpower.BACHELOR090_PDF)
def test_bachelor90page58_do_not_merge_caption(td, mp):
    """Do not merge figure caption into detected figure.

    One figure is composed out of lines and text.
    The other figure is an image figure and handled by rawmaker --images.
    """
    source = hoverpower.BACHELOR090_PDF
    pages = '58'
    tests.run(
        f'-i {source} -i {hoverpower.link(source)} --standard --pages={pages}',
        mp=mp,
    )
    names = utilo.file_list(td.tmpdir, include='png')
    bins = [utilo.file_read_binary(td.tmpdir.join(name)) for name in names]
    hashed = {utilotest.binhash(item) for item in bins}
    assert hashed == {154856633}


def test_master110page54(td, mp):
    images = tests.standard_figures(
        hoverpower.MASTER110_PDF,
        pages=54,
        td=td,
        mp=mp,
    )
    bounding = images[0].bounding
    expected = (64.65, 114.39, 516.75, 463.11)
    assert utilo.nears(bounding, expected)


@utilotest.longrun
def test_master110page2930(td, mp):
    images = tests.standard_figures(
        hoverpower.MASTER110_PDF,
        pages='29,30',
        td=td,
        mp=mp,
    )
    bounding = images[0].bounding
    expected = (129.24, 123.1, 479.75, 332.46)
    assert utilo.nears(bounding, expected)
    bounding = images[1].bounding
    expected = (115.2, 123.88, 465.81, 411.9)
    assert utilo.nears(bounding, expected)


@utilotest.longrun
def test_diss157p3536(td, mp):
    images = tests.standard_figures(
        hoverpower.DISS157_PDF,
        pages='35,36',
        td=td,
        mp=mp,
    )
    bounding = images[0].bounding
    expected = (217.12, 520.89, 399.89, 687.07)
    assert utilo.nears(bounding, expected)
    bounding = images[1].bounding
    expected = (141.97, 76.85, 472.55, 236.86)
    assert utilo.nears(bounding, expected)
