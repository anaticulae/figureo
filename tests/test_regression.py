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
    # TODO: INVESTIGATE WHERE DOE THESE RECTANGLES COME FROM!
    source = power.DISS266_PDF
    pages = '27,28,61'
    tests.run(f'-i {source} --standard --pages={pages}',
              monkeypatch=monkeypatch)
    # do not detect any figures on page 27, 28, 61
    assert not os.path.exists('figureo__standard_figures')


def test_nofigure_diss266_small_text_elements(testdir, monkeypatch):
    source = power.DISS266_PDF
    pages = '156,168,204'
    tests.run(f'-i {source} --standard --pages={pages}',
              monkeypatch=monkeypatch)
    assert not os.path.exists('figureo__standard_figures')


def test_figure_master155_page15(testdir, monkeypatch):
    source = power.MASTER155_PDF
    tests.run(f'-i {source} --standard --pages=15', monkeypatch=monkeypatch)
    imageinformation = serializeraw.images.load_image_informations_frompath(
        os.path.join(testdir.tmpdir, 'figureo__standard_figures'))
    assert len(imageinformation) == 1


def test_figure_master155_page17(testdir, monkeypatch):
    """Include lower 0, 5, 10 base."""
    pdf = power.MASTER155_PDF
    tests.run(f'-i {pdf} --standard --pages=17', monkeypatch=monkeypatch)
    imageinformation = serializeraw.images.load_image_informations_frompath(
        os.path.join(testdir.tmpdir, 'figureo__standard_figures'))
    assert len(imageinformation) == 1
    bounding = imageinformation[0].content[0].bounding
    expected = (155.76, 182.04, 528.05, 408.15)
    assert utila.nears(bounding, expected)
