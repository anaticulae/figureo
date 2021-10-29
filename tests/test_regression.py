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
import serializeraw.images
import utila
import utilatest

import tests


@utilatest.nightly
def test_extract_figures_memory_error(testdir, monkeypatch, capsys):
    # TODO: VALIDATE THIS UNIT TEST. THE MEMORY ERROR LOOKS QUITE
    # CONFUSING, PAY ATENTION TO THE PAGE NUMBERS
    source = power.BACHELOR085_PDF
    tests.run(f'-i {source}  --standard --pages=75:', monkeypatch=monkeypatch)
    stderr = utilatest.stderr(capsys)
    assert 'could not render' in stderr, str(stderr)


def test_nofigure_diss266_pagex(testdir, monkeypatch):
    # TODO: INVESTIGATE WHERE DOES THESE RECTANGLES COME FROM!
    source = power.DISS266_PDF
    pages = '27,28,61'
    tests.run(
        f'-i {source} --standard --pages={pages}',
        monkeypatch=monkeypatch,
    )
    # do not detect any figures on page 27, 28, 61
    assert not os.path.exists('rawmaker__images_images')


def test_nofigure_diss266_small_text_elements(testdir, monkeypatch):
    source = power.DISS266_PDF
    pages = '156,168,204'
    tests.run(
        f'-i {source} --standard --pages={pages}',
        monkeypatch=monkeypatch,
    )
    assert not os.path.exists('rawmaker__images_images')


def test_figure_master155_page15(testdir, monkeypatch):
    source = power.MASTER155_PDF
    tests.run(f'-i {source} --standard --pages=15', monkeypatch=monkeypatch)
    imageinformation = serializeraw.load_image_infos_frompath(
        testdir.tmpdir.join('rawmaker__images_images'))
    assert len(imageinformation) == 1


def test_figure_master155_page17(testdir, monkeypatch):
    """Include lower 0, 5, 10 base."""
    pdf = power.MASTER155_PDF
    tests.run(
        f'-i {pdf} -i {power.link(pdf)} --standard --pages=17',
        monkeypatch=monkeypatch,
    )
    imageinformation = serializeraw.load_image_infos_frompath(
        testdir.tmpdir.join('rawmaker__images_images'))
    assert len(imageinformation) == 1
    bounding = imageinformation[0].content[0].bounding
    expected = (155.76, 182.04, 514.03, 389.72)
    assert utila.nears(bounding, expected)


def test_bachelor90_whitepage_error(testdir, monkeypatch):
    """First page is a white page, this page produced an missing
    bounding error."""
    source = power.BACHELOR090_PDF
    pages = '0:10'
    tests.run(
        f'-i {source} -i{power.link(source)} --standard --pages={pages}',
        monkeypatch=monkeypatch,
    )


def test_bachelor90page58_do_not_merge_caption(testdir, monkeypatch):
    """Do not merge figure caption into detected figure.

    One figure is composed out of lines and text.
    The other figure is an image figure and handled by rawmaker --images.
    """
    source = power.BACHELOR090_PDF
    pages = '58'
    tests.run(
        f'-i {source} -i{power.link(source)} --standard --pages={pages}',
        monkeypatch=monkeypatch,
    )
    names = utila.file_list(testdir.tmpdir, include='png')
    bins = [
        utila.file_read_binary(os.path.join(testdir.tmpdir, name))
        for name in names
    ]
    hashed = {utilatest.binhash(item) for item in bins}
    assert hashed == {2827542461}
