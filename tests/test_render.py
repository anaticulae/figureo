# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw
import utila
import utilatest

import tests


def test_figures_run_bachelor56page27(td, mp):
    """Ensure that text below, left and right from figure is included
    into figure."""
    run_standard(power.BACHELOR056_PDF, pages=27, mp=mp)
    images = serializeraw.load_image_infos_frompath(
        td.tmpdir.join('rawmaker__images_images'))
    images = utila.flatten_content(images)
    assert len(images) == 1
    image = images[0]
    assert image.width >= 217, image.width
    assert image.height >= 158, image.height


def test_figures_run_bachelor56page19(td, mp):
    run_standard(power.BACHELOR056_PDF, pages=18, mp=mp)
    images = serializeraw.load_image_infos_frompath(
        td.tmpdir.join('rawmaker__images_images'))
    images = utila.flatten_content(images)
    assert len(images) == 1
    image = images[0]
    assert image.width >= 461, image.width
    assert image.height >= 39, image.height


@pytest.mark.usefixtures('testdir')
def test_figures_skip_dots(mp):
    images = run_standard(
        power.BACHELOR090_PDF,
        pages='81,82',
        mp=mp,
    )
    # do not generate any figure
    assert not images


def test_figures_skip_xml(td, mp):
    images = run_standard(
        power.BACHELOR067_PDF,
        pages='61',
        mp=mp,
    )
    print(utila.forward_slash(str(td.tmpdir)))
    # do not generate any figure
    assert not images


@pytest.mark.usefixtures('testdir')
@utilatest.requires(power.BACHELOR090_PDF)
def test_figures_double_image(mp):
    """This is an image, not a figure. We have to skip this."""
    images = run_standard(
        power.BACHELOR090_PDF,
        pages=80,
        mp=mp,
    )
    # do not generate any figure
    assert not images


@pytest.mark.usefixtures('testdir')
def test_reg_figure_text_in_figure(mp):
    """Do not include `Diplomarbeit` inside title page figure."""
    images = run_standard(power.MASTER078_PDF, pages=0, mp=mp)
    image = images[0]
    assert image.height < 140.0, f'Diplomarbeit included: {image.height}'


@pytest.mark.usefixtures('testdir')
def test_master31page4(mp):
    images = run_standard(power.MASTER031_PDF, pages=4, mp=mp)
    selected = images[0].bounding
    expected = (297.36, 66.0, 532.92, 257.28)
    assert utila.nears(selected, expected, diff=5.0)


@pytest.mark.usefixtures('testdir')
def test_master31page10(mp):
    """Detect single figure.

    Two Asian characters are handled by rawmaker --image.
    """
    images = run_standard(
        power.MASTER031_PDF,
        pages=10,
        mp=mp,
    )
    assert len(images) == 1  # pylint:disable=C2001
    selected = images[0].bounding
    expected = (71.61, 415.7, 524.5, 556.19)
    assert utila.nears(selected, expected, diff=4.0)


@utilatest.longrun
@pytest.mark.usefixtures('testdir')
def test_master75page1718(mp):
    images = run_standard(
        power.MASTER075_PDF,
        pages='17,18',
        mp=mp,
    )
    # page17
    bounding = images[0].bounding
    expected = (70.85, 135.41, 452.0, 717.15)
    assert utila.nears(bounding, expected)
    # page18
    bounding = images[1].bounding
    expected = (70.85, 73.3, 416.39, 725.25)
    assert utila.nears(bounding, expected)


@pytest.mark.usefixtures('testdir')
def test_bachelor51page29(mp):
    images = run_standard(
        power.BACHELOR051_PDF,
        pages=29,
        mp=mp,
    )
    selected = images[0].bounding
    expected = (86.16, 56.28, 440.16, 281.28)
    assert utila.nears(selected, expected)


@pytest.mark.usefixtures('testdir')
def test_bachelor37page18(mp):
    """Do not increase valid_area tolerance too much to avoid including
    parts of header and footer into extracted figures."""
    images = run_standard(
        power.BACHELOR037_PDF,
        pages=18,
        mp=mp,
    )
    selected = images[0].bounding
    expected = (95.03, 63.46, 514.56, 210.87)
    assert utila.nears(selected, expected)


@pytest.mark.usefixtures('testdir')
def test_bachelor37page23(mp):
    images = run_standard(
        power.BACHELOR037_PDF,
        pages=23,
        mp=mp,
    )
    boundings = sorted([image.bounding for image in images])
    expected = [(65.52, 559.2, 529.92, 632.27), (70.92, 253.19, 510.36, 383.16)]
    assert utila.nears(boundings[0], expected[0])
    assert utila.nears(boundings[1], expected[1])


@pytest.mark.usefixtures('testdir')
def test_diss205p102(mp):
    images = run_standard(
        power.DISS205_PDF,
        pages=102,
        mp=mp,
    )
    selected = images[0].bounding
    expected = (179.13, 250.27, 406.71, 437.01)
    assert utila.nears(selected, expected)


@pytest.mark.usefixtures('testdir')
def test_diss205p141(mp):
    images = run_standard(
        power.DISS205_PDF,
        pages=141,
        mp=mp,
    )
    selected = images[0].bounding
    expected = (81.23, 309.1, 505.51, 450.41)
    assert utila.nears(selected, expected)


# yapf:disable
@pytest.mark.parametrize('page, expected', [
    pytest.param(13, (126.27, 113.8, 497.37, 428.8), id='page13'),
    pytest.param(15, (126.41, 113.93, 497.23, 231.3), id='page15'),
    pytest.param(16, (188.25, 591.37, 435.37, 625.48), id='page16'),
    pytest.param(17, [(126.42, 153.29, 497.22, 189.96), (126.42, 319.85, 497.22, 365.6)], id='page17'),
    pytest.param(19, (126.41, 113.93, 497.23, 253.93), id='page19'),
    pytest.param(21, [(105.66, 386.18, 517.97, 646.18), (105.66, 167.68, 517.97, 337.68)], id='page21'),
    pytest.param(48, (110.29, 515.85, 511.84, 645.85), id='page48'),
    pytest.param(52, [(112.74, 177.94, 510.1, 334.1), (109.25, 423.09, 510.7, 578.09)], id='page52'),
])
# yapf:enable
def test_bachelor67pagex(page, expected, td, mp):  # pylint:disable=W0613
    """\
    page15: Detect single text figures which are build out of a single LTFigure.
    page48: Shrink figure size which is badly printed by pdfprinter.
    """
    verify(power.BACHELOR067_PDF, page, expected, mp)


@pytest.mark.usefixtures('testdir')
def test_master063p25(mp):
    images = run_standard(
        power.MASTER063_PDF,
        pages=25,
        mp=mp,
    )
    selected = images[0].bounding
    expected = (70.85, 277.83, 408.35, 451.08)
    assert utila.nears(selected, expected)


def verify(source, page, expected, mp):
    images = run_standard(
        source=source,
        pages=page,
        mp=mp,
    )
    if isinstance(expected, tuple):
        expected = [expected]
    for figure, expect in zip(images, expected):
        assert utila.nears(figure.bounding, expect, diff=5.0)


def run_standard(source, pages, mp) -> list:
    utilatest.fixture_requires(source)
    cmd = f'-i {source} --pages={pages} --standard'
    source = power.link(source)
    if os.path.exists(source):
        cmd = f'{cmd} -i {source}'
    tests.run(cmd, mp=mp)
    if not os.path.exists('rawmaker__images_images'):
        return []
    images = serializeraw.load_image_infos_frompath('rawmaker__images_images')
    result = utila.flatten_content(images)
    return result
