#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import functools

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
