#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utilo
import utilo.cli

import figureo

DESCRIPTION = """
"""

# yapf:disable
WORKPLAN = [
    utilo.create_step(
        'standard',
        inputs=[
            utilo.Pattern('*', 'pdf'),
            utilo.ResultFile(producer='groupme', name='content_content', optional=True),
            utilo.ResultFile(producer='tablero', name='decide_decide', optional=True),
            utilo.ResultFile(producer='rawmaker', name='formula_formula', optional=True),
        ],
        output=[
            ('figures/{FILEHASH_1}', 'yaml'),
            ('figures/{FILEHASHS}', 'png'),
        ],
    ),
    utilo.create_step(
        'cleanup',
        inputs=[
            utilo.ResultFile(producer='figureo', name='standard_standard', optional=True),
            utilo.Pattern(name='rawmaker__images_images/*', ext='yaml'),
        ],
        output=[
            '{FILEPATHS}',
        ],
    ),
]
# yapf:enable


@utilo.saveme
def main():
    config = utilo.FeaturePackConfig(
        configflag=True,
        description=DESCRIPTION,
        multiprocessed=True,
        name=figureo.PROCESS,
        pages=True,
        profileflag=True,
        singleinput=True,
        verboseflag=True,
        rename=rename,
        version=figureo.__version__,
    )
    utilo.featurepack(
        workplan=WORKPLAN,
        config=config,
        root=figureo.ROOT,
        featurepackage='figureo.features',
    )


def rename(path):
    if not isinstance(path, str):
        path = [rename(item) for item in path]
        return path
    path = utilo.rreplace(
        path,
        pattern='figureo__standard_figures',
        replace='rawmaker__images_images',
    )
    return path
