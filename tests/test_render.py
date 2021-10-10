# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
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


@pytest.mark.usefixtures('testdir')
def test_figures_run_bachelor56page27(monkeypatch):
    """Ensure that text below, left and right from figure is included
    into figure."""
    run_standard(power.BACHELOR056_PDF, pages=27, monkeypatch=monkeypatch)
    expected_file_count = 1
    figure = 'rawmaker__images_images'
    written = utila.file_list(figure, include='yaml')
    assert len(written) == expected_file_count, str(written)
    path = os.path.join(figure, written[0])
    image = serializeraw.load_image_info(path)
    assert image.width >= 221, image.width
    assert image.height >= 163, image.height


@pytest.mark.usefixtures('testdir')
def test_figures_skip_dots(monkeypatch):
    images = run_standard(
        power.BACHELOR090_PDF,
        pages='81,82',
        monkeypatch=monkeypatch,
    )
    # do not generate any figure
    assert not images


@pytest.mark.usefixtures('testdir')
@utilatest.requires(power.BACHELOR090_PDF)
def test_figures_double_image(monkeypatch):
    """This is an image, not a figure. We have to skip this."""
    images = run_standard(
        power.BACHELOR090_PDF,
        pages=80,
        monkeypatch=monkeypatch,
    )
    # do not generate any figure
    assert not images


def test_reg_figure_text_in_figure(testdir, monkeypatch):
    """Do not include `Diplomarbeit` inside title page figure."""
    images = run_standard(power.MASTER078_PDF, pages=0, monkeypatch=monkeypatch)
    image = images[0].content[0]
    assert image.height < 140.0, f'Diplomarbeit included: {image.height}'


def test_master31page4(testdir, monkeypatch):
    images = run_standard(power.MASTER031_PDF, pages=4, monkeypatch=monkeypatch)
    selected = images[0].content[0].bounding
    expected = (305.57, 67.33, 526.39, 251.31)
    assert selected == expected


def test_master31page10(testdir, monkeypatch):
    """Detect single figure.

    Two Asian characters are handled by rawmaker --image.
    """
    images = run_standard(
        power.MASTER031_PDF,
        pages=10,
        monkeypatch=monkeypatch,
    )
    assert len(images) == 1  # pylint:disable=C2001
    selected = images[0].content[0].bounding
    expected = (71.61, 415.7, 524.5, 556.19)
    assert selected == expected


def test_master75page1718(testdir, monkeypatch):
    images = run_standard(
        power.MASTER075_PDF,
        pages='17,18',
        monkeypatch=monkeypatch,
    )
    # page17
    bounding = images[0].content[0].bounding
    expected = (70.85, 135.41, 452.0, 715.99)
    assert bounding == expected
    # page18
    bounding = images[1].content[0].bounding
    expected = (70.85, 73.3, 416.39, 725.25)
    assert bounding == expected


def test_bachelor51page29(testdir, monkeypatch):
    images = run_standard(
        power.BACHELOR051_PDF,
        pages=29,
        monkeypatch=monkeypatch,
    )
    selected = images[0].content[0].bounding
    expected = (86.16, 56.28, 440.16, 281.28)
    assert selected == expected


def test_bachelor37page18(testdir, monkeypatch):
    """Do not increase valid_area tolerance too much to avoid including
    parts of header and footer into extracted figures."""
    images = run_standard(
        power.BACHELOR037_PDF,
        pages=18,
        monkeypatch=monkeypatch,
    )
    selected = images[0].content[0].bounding
    expected = (95.03, 63.46, 514.56, 210.87)
    assert selected == expected


def run_standard(source, pages, monkeypatch) -> list:
    cmd = f'-i {source} --pages={pages} --standard'
    source = power.link(source)
    if os.path.exists(source):
        cmd = f'{cmd} -i {source}'
    tests.run(cmd, monkeypatch=monkeypatch)
    if not os.path.exists('rawmaker__images_images'):
        return []
    images = serializeraw.load_image_infos_frompath('rawmaker__images_images')
    return images
