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


@pytest.mark.xfail(reason='improve parser')
@pytest.mark.usefixtures('testdir')
def test_figures_skip_dots(monkeypatch):
    run_standard(power.BACHELOR090_PDF, pages='81,82', monkeypatch=monkeypatch)
    figure = 'rawmaker__images_images'
    # do not generate any figure
    assert not os.path.exists(figure)


@pytest.mark.usefixtures('testdir')
@utilatest.requires(power.BACHELOR090_PDF)
def test_figures_double_image(monkeypatch):
    """This is an image, not a figure. We have to skip this."""
    run_standard(power.BACHELOR090_PDF, pages=80, monkeypatch=monkeypatch)
    figure = 'rawmaker__images_images'
    # do not generate any figure
    assert not os.path.exists(figure)


def run_standard(source, pages, monkeypatch):
    cmd = f'-i {source} --pages={pages} --standard'
    source = power.link(source)
    if os.path.exists(source):
        cmd = f'{cmd} -i {source}'
    tests.run(cmd, monkeypatch=monkeypatch)


def test_reg_figure_text_in_figure(testdir, monkeypatch):
    """Do not include `Diplomarbeit` inside title page figure."""
    run_standard(power.MASTER078_PDF, pages=0, monkeypatch=monkeypatch)
    images = serializeraw.load_image_infos_frompath('rawmaker__images_images')
    image = images[0].content[0]
    assert image.height < 140.0, f'Diplomarbeit included: {image.height}'
