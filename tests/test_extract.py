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
    content = power.link(source)
    if pages is None:
        pages = (12, 13)
    extracted = figureo.features.standard.work(source, content, pages=pages)
    assert extracted
    return extracted


def standard_figures(pdf, pages: str, testdir, monkeypatch):
    source = power.link(pdf)
    cmd = f'-i {pdf} -i {source} -o {testdir.tmpdir} --pages={pages} --standard'
    tests.run(cmd, monkeypatch=monkeypatch)
    if not utila.exists('rawmaker__images_images'):
        return []
    # verify
    written = utila.file_list('rawmaker__images_images')
    return written


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


@utilatest.longrun
def test_figures_run_master116(monkeypatch, testdir):
    written = standard_figures(
        power.MASTER116_PDF,
        '17:24',
        testdir,
        monkeypatch,
    )
    # verify
    expected_file_count = 7 * 2
    assert len(written) == expected_file_count, str(written)


def test_figures_run_master116page18(monkeypatch, testdir):
    written = standard_figures(
        power.MASTER116_PDF,
        18,
        testdir,
        monkeypatch,
    )
    assert len(written) == 2, str(written)


def test_render_master116_page2_figure_image(monkeypatch, testdir):
    """Figure image is handled by rawmaker --images."""
    written = standard_figures(power.MASTER116_PDF, 2, testdir, monkeypatch)
    assert not written


@pytest.mark.parametrize('page, expected', [
    (23, 1),
    (39, 1),
    (44, 1),
    (45, 1),
    (56, 1),
    (57, 1),
    (58, 1),
])
def test_render_bachelor90_pagex_figure(page, expected, monkeypatch, testdir):
    written = standard_figures(
        power.BACHELOR090_PDF,
        page,
        testdir,
        monkeypatch,
    )
    # png and yaml files
    expected = expected * 2
    assert len(written) == expected, str(written)


@pytest.mark.xfail(reason='improve table parser')
def test_render_bachelor51_page30_33_figure_image(monkeypatch, testdir):
    """Detect two nearly equal figures on different pages.

    Ensure that tables on the same page are not located as figure anymore.
    """
    written = standard_figures(
        power.BACHELOR051_PDF,
        '30,33',
        testdir,
        monkeypatch,
    )
    # 2 png and 2 yaml files
    expected = 4
    assert len(written) == expected, str(written)


def test_render_diss172page30(monkeypatch, testdir):
    """Single image which intersects page border."""
    written = standard_figures(
        power.DISS172_PDF,
        '30',
        testdir,
        monkeypatch,
    )
    # 1 png and 1 yaml files
    expected = 2
    assert len(written) == expected, str(written)
