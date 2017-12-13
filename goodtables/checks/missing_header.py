# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from copy import copy
from ..registry import check
from ..error import Error


# Module API

@check('missing-header', type='schema', context='head')
def missing_header(cells, sample=None):
    errors = []

    for cell in copy(cells):

        # Skip if header in cell
        if 'header' in cell:
            continue

        # Add error
        error = Error('missing-header', cell)
        errors.append(error)

        # Remove cell
        cells.remove(cell)

    return errors
