# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import pytest
import utilotest

import tests


@pytest.mark.usefixtures('td')
@pytest.mark.parametrize('source, pages', [
    pytest.param(
        hoverpower.DISS266_PDF, '156,168,204', id='small_text_elements'),
    pytest.param(hoverpower.DISS266_PDF, '27,28,61', id='diss266'),
    pytest.param(hoverpower.HOME050_PDF, '31', id='home50p31_formula'),
    pytest.param(hoverpower.MASTER091B_PDF, '19', id='master091bp19'),
])
def test_nofigure(source, pages, mp):
    utilotest.fixture_requires(source)
    generated = hoverpower.link(source)
    tests.run(
        f'-i {generated} -i {source} --standard --pages={pages}',
        mp=mp,
    )
    assert not os.path.exists('rawmaker__images_images')
