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

# yapf:disable
WORKPLAN = [
    utila.create_step(
        'standard',
        inputs=[
            utila.Pattern('*', 'pdf'),
            utila.ResultFile(producer='groupme', name='content_content', optional=True),
            utila.ResultFile(producer='tablero', name='decide_decide', optional=True),
            utila.ResultFile(producer='rawmaker', name='formula_formula', optional=True),
        ],
        output=[
            ('figures/{FILEHASH_1}', 'yaml'),
            ('figures/{FILEHASHS}', 'png'),
        ],
    ),
    utila.create_step(
        'cleanup',
        inputs=[
            utila.ResultFile(producer='figureo', name='standard_standard', optional=True),
            utila.Pattern(name='rawmaker__images_images/*', ext='yaml'),
        ],
        output=[
            '{FILEPATHS}',
        ],
    ),
]
# yapf:enable


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
        rename=rename,
        version=figureo.__version__,
    )
    utila.featurepack(
        workplan=WORKPLAN,
        config=config,
        root=figureo.ROOT,
        featurepackage='figureo.features',
    )


def rename(path):
    if not isinstance(path, str):
        path = [rename(item) for item in path]
        return path
    path = utila.rreplace(
        path,
        pattern='figureo__standard_figures',
        replace='rawmaker__images_images',
    )
    return path
