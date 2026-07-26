# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

hoverpower.setup(__file__)

RESOURCES = [
    (hoverpower.DISS143_PDF, '25'),
    (hoverpower.DISS157_PDF, '30:40'),
    (hoverpower.DISS172_PDF, '30'),
    (hoverpower.DISS205_PDF, '100:110,140:145'),
    (hoverpower.DISS266_PDF, '25:30,55:65,150:160,200:210'),
    (hoverpower.HOME050_PDF, '31'),
    (hoverpower.MASTER031_PDF, '5:20'),
    (hoverpower.MASTER063_PDF, '20:30'),
    (hoverpower.MASTER075_PDF, '10:25'),
    (hoverpower.MASTER078_PDF, '0:10'),
    (hoverpower.MASTER091B_PDF, '19'),
    (hoverpower.MASTER105_PDF, '30:40'),
    (hoverpower.MASTER110_PDF, '29:40,54'),
    (hoverpower.MASTER116_PDF, '10:30'),
    hoverpower.BACHELOR037_PDF,
    hoverpower.BACHELOR051_PDF,
    hoverpower.BACHELOR056_PDF,
    hoverpower.BACHELOR067_PDF,
    hoverpower.BACHELOR085_PDF,
    hoverpower.BACHELOR090_PDF,
    hoverpower.MASTER155_PDF,
]

WORKER = utilotest.worker_count(7, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    gennex.extract(
        files=resources,
        cleanup=True,
        footnote=True,
        # formulero=True,
        groupme='--border --content',
        headnote=True,
        oneline=None,
        pagenumber=True,
        tablero=True,
        pages=':',
        worker=WORKER,
    )
