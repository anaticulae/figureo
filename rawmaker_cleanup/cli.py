# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import argparse
import os
import sys

import utila

DESCRIPTION = """\
Load PageTextNavigators, figures and tables.

It removes text which is inside figures and or tables and writes
PageTextNavigators afterwards.
"""


@utila.saveme
def main():
    # parameter = user_input()
    sys.exit(utila.SUCCESS)


def user_input() -> tuple:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-i',
        dest='inpath',
        default=os.getcwd(),
    )
    parser.add_argument(
        '-o',
        dest='outpath',
        default=os.path.join(os.getcwd(), 'outpath'),
    )
    args = parser.parse_args()
    inpath, outpath = args.inpath, args.outpath
    return inpath, outpath
