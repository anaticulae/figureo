#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import importlib.metadata
import os

import figureo.__patch__

PROCESS = 'figureo'
__version__ = importlib.metadata.version(PROCESS)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
