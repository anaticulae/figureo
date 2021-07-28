# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import figureo.features.standard
import tests


def extract_figures(pages=None):
    """2 Figures on page 12 and 1 figure and 1 image on page 13."""
    source = power.MASTER116_PDF
    if pages is None:
        pages = (12, 13)
    extracted = figureo.features.standard.work(source, pages=pages)
    assert extracted
    return extracted


def test_figures_extract():
    extracted = extract_figures()
    assert len(extracted) == 3, str(extracted)


def test_figures_dump_and_load(testdir):
    outpath = testdir.tmpdir
    extracted = extract_figures()
    # 3 figures and 3 information
    with utilatest.increased_filecount(outpath, mindiff=6, maxdiff=6):
        serializeraw.dump_figures(extracted, outpath)

    loaded = serializeraw.load_figures(outpath)
    assert len(loaded) == 3


def test_figures_extract_master116_page19(testdir):
    outpath = testdir.tmpdir
    extracted = extract_figures((19, 38))
    # 3 figures and 3 information
    with utilatest.increased_filecount(outpath, mindiff=6, maxdiff=6):
        serializeraw.dump_figures(extracted, outpath)


@pytest.mark.xfail(reason='table on page 20 is detected is figure')
@utilatest.longrun
@pytest.mark.usefixtures('testdir')
def test_figures_run_master116(monkeypatch):
    source = power.MASTER116_PDF
    cmd = f'-i {source} --pages=17:24 --standard'
    tests.run(cmd, monkeypatch=monkeypatch)

    expected_file_count = 7 * 2
    written = utila.file_list('figureo__standard_figures')
    assert len(written) == expected_file_count, str(written)


def test_render_master116_page18(monkeypatch, testdir):
    source = power.MASTER116_PDF
    cmd = f'-i {source} --pages=18 --standard'
    tests.run(cmd, monkeypatch=monkeypatch)

    written = utila.file_list('figureo__standard_figures')
    # 2 png and 2 yaml files
    expected = 4
    assert len(written) == expected, str(written)


def test_render_master116_page2_figure_image(monkeypatch, testdir):
    written = extract(power.MASTER116_PDF, 2, monkeypatch)
    # 1 png and 1 yaml files
    expected = 2
    assert len(written) == expected, str(written)


# TODO: 58, 2 reduce later to 1
@pytest.mark.parametrize('page, expected', [
    (23, 1),
    (39, 1),
    (44, 1),
    (45, 1),
    (56, 1),
    (57, 1),
    (58, 2),
])
def test_render_bachelor90_pagex_figure(page, expected, monkeypatch, testdir):
    written = extract(power.BACHELOR090_PDF, page, monkeypatch)
    # png and yaml files
    expected = expected * 2
    assert len(written) == expected, str(written)


def test_render_bachelor51_page30_33_figure_image(monkeypatch, testdir):
    """The figure name is determined dues hashing the figure content. If
    both figures are equal(empty and same size for example) the figures
    have the same name and one image information is lost. Therefore we
    include the pageid id into a central pixel in the middle of the
    figure. As a result of this, we do not lose bounding information."""
    written = extract(power.BACHELOR051_PDF, '30,33', monkeypatch)
    # 3 png and 3 yaml files
    # correct is 2 because 1 table is detected as figure
    expected = 8
    assert len(written) == expected, str(written)


def extract(source, pages, monkeypatch) -> list:
    cmd = f'-i {source} --pages={pages} --standard'
    tests.run(cmd, monkeypatch=monkeypatch)
    written = utila.file_list('figureo__standard_figures')
    return written
