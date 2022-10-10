# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import figureo

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = figureo.PROCESS

power.setup(figureo.ROOT)
RESOURCES = [
    (power.DISS143_PDF, '25'),
    (power.DISS157_PDF, '30:40'),
    (power.DISS172_PDF, '30'),
    (power.DISS205_PDF, '100:110,140:145'),
    (power.HOME050_PDF, '31'),
    (power.MASTER031_PDF, '5:20'),
    (power.MASTER063_PDF, '20:30'),
    (power.MASTER075_PDF, '10:25'),
    (power.MASTER091B_PDF, '19'),
    (power.MASTER105_PDF, '30:40'),
    (power.MASTER110_PDF, '29:40,54'),
    power.BACHELOR037_PDF,
    power.BACHELOR051_PDF,
    power.BACHELOR056_PDF,
    power.BACHELOR067_PDF,
    power.BACHELOR085_PDF,
    power.BACHELOR090_PDF,
    power.DISS266_PDF,
    power.MASTER116_PDF,
    power.MASTER155_PDF,
]

WORKER = utilatest.worker_count(7, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        files=resources,
        groupme='--border --content',
        cleanup=True,
        footnote=True,
        formulero=True,
        headnote=True,
        oneline=None,
        pagenumber=True,
        tablero=True,
        pages=':',
        worker=WORKER,
    )
