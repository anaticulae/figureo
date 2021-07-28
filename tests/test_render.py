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

import tests


@pytest.mark.usefixtures('testdir')
def test_figures_run_bachelor56page27(monkeypatch):
    """Ensure that text below, left and right from figure is included
    into figure."""
    source = power.BACHELOR056_PDF
    cmd = f'-i {source} --pages=27 --standard'
    tests.run(cmd, monkeypatch=monkeypatch)

    expected_file_count = 1
    figure = 'figureo__standard_figures'
    written = utila.file_list(figure, include='yaml')
    assert len(written) == expected_file_count, str(written)

    path = os.path.join(figure, written[0])
    image = serializeraw.load_image_info(path)
    assert image.width >= 221, image.width
    assert image.height >= 163, image.height
