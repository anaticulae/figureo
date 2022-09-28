# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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
    utilatest.fixture_requires(source)
    content = power.link(source)
    if pages is None:
        pages = (12, 13)
    extracted = figureo.features.standard.work(source, content, pages=pages)
    assert extracted
    return extracted


def standard_figures(pdf, pages: str, td, mp):
    utilatest.fixture_requires(pdf)
    source = power.link(pdf)
    cmd = f'-i {pdf} -i {source} -o {td.tmpdir} --pages={pages} --standard'
    tests.run(cmd, mp=mp)
    if not utila.exists('rawmaker__images_images'):
        return []
    # verify
    written = utila.file_list('rawmaker__images_images')
    return written


@utilatest.longrun
def test_figures_extract():
    extracted = extract_figures()
    assert len(extracted) == 3, str(extracted)


@utilatest.longrun
def test_figures_dump_and_load(td):
    outpath = td.tmpdir
    extracted = extract_figures()
    # 3 figures and 3 information
    with utilatest.increased_filecount(outpath, mindiff=6, maxdiff=6):
        serializeraw.dump_figures(extracted, outpath)
    loaded = serializeraw.load_figures(outpath)
    assert len(loaded) == 3


@utilatest.longrun
def test_figures_extract_master116_page19(td):
    outpath = td.tmpdir
    extracted = extract_figures((19, 38))
    # 3 figures and 3 information
    with utilatest.increased_filecount(outpath, mindiff=6, maxdiff=6):
        serializeraw.dump_figures(extracted, outpath)


@utilatest.longrun
def test_figures_run_master116(mp, td):
    written = standard_figures(
        power.MASTER116_PDF,
        '17:24',
        td,
        mp,
    )
    # verify
    expected_file_count = 7 * 2
    assert len(written) == expected_file_count, str(written)


def test_figures_run_master116page18(mp, td):
    written = standard_figures(
        power.MASTER116_PDF,
        18,
        td,
        mp,
    )
    assert len(written) == 2, str(written)


def test_render_master116_page2_figure_image(mp, td):
    """Figure image is handled by rawmaker --images."""
    written = standard_figures(power.MASTER116_PDF, 2, td, mp)
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
def test_render_bachelor90_pagex_figure(page, expected, mp, td):
    written = standard_figures(
        power.BACHELOR090_PDF,
        page,
        td,
        mp,
    )
    # png and yaml files
    expected = expected * 2
    assert len(written) == expected, str(written)


@pytest.mark.xfail(reason='improve table parser')
@utilatest.longrun
def test_render_bachelor51_page30_33_figure_image(mp, td):
    """Detect two nearly equal figures on different pages.

    Ensure that tables on the same page are not located as figure anymore.
    """
    written = standard_figures(
        power.BACHELOR051_PDF,
        '30,33',
        td,
        mp,
    )
    # 2 png and 2 yaml files
    expected = 4
    assert len(written) == expected, str(written)


def test_render_diss172page30(mp, td):
    """Single image which intersects page border."""
    written = standard_figures(
        power.DISS172_PDF,
        '30',
        td,
        mp,
    )
    # 1 png and 1 yaml files
    expected = 2
    assert len(written) == expected, str(written)
