#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila
import utila.cli

from figureo import __version__

COMMANDS = []  # add additional commands here


@utila.saveme
def main():
    parser = utila.cli.create_parser(
        COMMANDS,
        version=__version__,
        config=utila.ParserConfiguration(
            outputparameter=True,
            inputparameter=True,
        ),
    )
    args = utila.parse(parser)
    inputpath, output, _ = utila.sources(args)  # pylint:disable=W0612,W0632
    return utila.SUCCESS
