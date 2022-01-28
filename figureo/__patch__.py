# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdfminer.layout


def __getitem__(self, index):
    return self._objs[index]  # pylint:disable=W0212


pdfminer.layout.LTFigure.__getitem__ = __getitem__


def __len__(self):
    return len(self._objs)  # pylint:disable=W0212


pdfminer.layout.LTFigure.__len__ = __len__
