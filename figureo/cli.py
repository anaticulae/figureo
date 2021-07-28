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

import figureo

DESCRIPTION = """
"""

WORKPLAN = [
    utila.create_step(
        'standard',
        inputs=[
            utila.Pattern('*', 'pdf'),
            utila.ResultFile(
                producer='groupme',
                name='content_content',
                optional=True,
            ),
        ],
        output=[
            ('figures/{FILEHASH_1}', 'yaml'),
            ('figures/{FILEHASHS}', 'png'),
        ],
    ),
]


@utila.saveme
def main():
    config = utila.FeaturePackConfig(
        configflag=True,
        description=DESCRIPTION,
        multiprocessed=True,
        name=figureo.PROCESS,
        pages=True,
        profileflag=True,
        singleinput=True,
        verboseflag=True,
        version=figureo.__version__,
    )
    utila.featurepack(
        workplan=WORKPLAN,
        config=config,
        root=figureo.ROOT,
        featurepackage='figureo.features',
    )
