# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest

import figureo

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = figureo.PROCESS
WORKER = 4

power.setup(figureo.ROOT)

RESOURCES = [
    power.BACHELOR051_PDF,
    power.BACHELOR056_PDF,
    power.BACHELOR085_PDF,
    power.BACHELOR090_PDF,
    power.BACHELOR037_PDF,
    power.DISS266_PDF,
    power.MASTER116_PDF,
    power.MASTER155_PDF,
    power.BACHELOR067_PDF,
    (power.MASTER075_PDF, '10:25'),
    (power.DISS157_PDF, '30:40'),
    (power.MASTER110_PDF, '29:40,54'),
    (power.DISS172_PDF, '30'),
    (power.DISS143_PDF, '25'),
    (power.HOME050_PDF, '31'),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        files=resources,
        destination=power.generated(),
        groupme='--pagenumbers --border --footer --content',
        oneline=None,
        tablero=True,
        formulero=True,
        pages=':',
        worker=WORKER,
        base=power.REPOSITORY,
    )
