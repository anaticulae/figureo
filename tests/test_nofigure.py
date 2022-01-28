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

import tests


@pytest.mark.parametrize('source, pages', [
    pytest.param(power.DISS266_PDF, '27,28,61', id='diss266'),
    pytest.param(
        power.DISS266_PDF,
        '156,168,204',
        id='diss266_small_text_elements',
    ),
    pytest.param(power.HOME050_PDF, '31', id='home50p31_formula'),
])
def test_nofigure(source, pages, testdir, monkeypatch):
    generated = power.link(source)
    tests.run(
        f'-i {generated} -i {source} --standard --pages={pages}',
        monkeypatch=monkeypatch,
    )
    assert not os.path.exists('rawmaker__images_images')
