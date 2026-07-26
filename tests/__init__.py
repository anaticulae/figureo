#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import functools

import hoverpower
import serializeraw
import utilo
import utilotest

import figureo
import figureo.cli

#pylint: disable=invalid-name
run = functools.partial(
    utilotest.run_command,
    main=figureo.cli.main,
    process=figureo.PROCESS,
    expect=True,
)

failure = functools.partial(
    utilotest.run_command,
    main=figureo.cli.main,
    process=figureo.PROCESS,
    expect=False,
)


def standard_figures(pdf, pages: str, td, mp):
    utilotest.fixture_requires(pdf)
    source = hoverpower.link(pdf)
    cmd = f'-i {pdf} -i {source} -o {td.tmpdir} --pages={pages} --standard'
    run(cmd, mp=mp)
    if not utilo.exists('rawmaker__images_images'):
        return []
    # verify
    written = serializeraw.load_image_infos_frompath(
        td.tmpdir.join('rawmaker__images_images'))
    result = utilo.flatten_content(written)
    return result
