# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw
import utila
import utilatest

import tests
import tests.test_render


@utilatest.requires(power.BACHELOR051_PDF)
def test_bachelor51page29_cleanup(td, mp):
    generated = os.path.join(
        power.link(power.BACHELOR051_PDF),
        'rawmaker__images_images',
    )
    tests.test_render.run_standard(
        power.BACHELOR051_PDF,
        pages=29,
        mp=mp,
    )
    utila.copy_content(
        generated,
        td.tmpdir.join('rawmaker__images_images'),
        unlock=True,
    )
    run_cleanup(
        path=td.tmpdir,
        pages=29,
        mp=mp,
    )
    images = serializeraw.load_image_infos_frompath('rawmaker__images_images')
    # ensure that some images are hidden by extract figure
    assert any(item.hidden for item in utila.flatten_content(images))


def run_cleanup(path, pages, mp) -> list:
    cmd = f'-i {path} -o {path} --pages={pages} --cleanup'
    tests.run(cmd, mp=mp)
    if not os.path.exists('rawmaker__images_images'):
        return []
    images = serializeraw.load_image_infos_frompath('rawmaker__images_images')
    return images


@pytest.mark.xfail(reason='new software')
@utilatest.longrun
@utilatest.requires(power.BACHELOR051_PDF)
def test_bachelor51p30_hide_images(td, mp):
    pdf = power.BACHELOR051_PDF
    utila.run(f'rawmaker -i {pdf} --images --pages=30 -o {td.tmpdir}')
    workdir = td.tmpdir.join('rawmaker__images_images')
    cmd = f'-i {pdf} -i {workdir} -i {td.tmpdir} -o {td.tmpdir} --pages=30'
    tests.run(cmd, mp=mp)
    images = serializeraw.load_image_infos_frompath(workdir)
    images = utila.flatten_content(images)
    hidden = [item for item in images if item.hidden]
    assert len(hidden) == 4
