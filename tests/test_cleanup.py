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
import serializeraw
import utila

import tests
import tests.test_render


def test_bachelor51page29_cleanup(testdir, monkeypatch):
    generated = os.path.join(
        power.link(power.BACHELOR051_PDF),
        'rawmaker__images_images',
    )
    tests.test_render.run_standard(
        power.BACHELOR051_PDF,
        pages=29,
        monkeypatch=monkeypatch,
    )
    utila.copy_content(generated, testdir.tmpdir.join('rawmaker__images_images'))  # yapf:disable
    run_cleanup(
        path=testdir.tmpdir,
        pages=29,
        monkeypatch=monkeypatch,
    )
    images = serializeraw.load_image_infos_frompath('rawmaker__images_images')
    # ensure that some images are hidden by extract figure
    assert any(item.hidden for item in utila.flatten_content(images))


def run_cleanup(path, pages, monkeypatch) -> list:
    cmd = f'-i {path} -o {path} --pages={pages} --cleanup'
    tests.run(cmd, monkeypatch=monkeypatch)
    if not os.path.exists('rawmaker__images_images'):
        return []
    images = serializeraw.load_image_infos_frompath('rawmaker__images_images')
    return images
