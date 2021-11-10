#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import functools

import power
import serializeraw
import utila
import utilatest

import figureo
import figureo.cli

#pylint: disable=invalid-name
run = functools.partial(
    utilatest.run_command,
    main=figureo.cli.main,
    process=figureo.PROCESS,
    success=True,
)

failure = functools.partial(
    utilatest.run_command,
    main=figureo.cli.main,
    process=figureo.PROCESS,
    success=False,
)


def standard_figures(pdf, pages: str, testdir, monkeypatch):
    source = power.link(pdf)
    cmd = f'-i {pdf} -i {source} -o {testdir.tmpdir} --pages={pages} --standard'
    run(cmd, monkeypatch=monkeypatch)
    if not utila.exists('rawmaker__images_images'):
        return []
    # verify
    written = serializeraw.load_image_infos_frompath(
        testdir.tmpdir.join('rawmaker__images_images'))
    result = utila.flatten_content(written)
    return result
