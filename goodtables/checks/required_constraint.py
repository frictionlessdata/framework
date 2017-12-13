# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from copy import copy
from ..registry import check
from ..error import Error


# Module API

@check('required-constraint', type='schema', context='body')
def required_constraint(cells, row_number):
    errors = []

    for cell in copy(cells):

        # Skip if cell is incomplete
        if not set(cell).issuperset(['number', 'header', 'field', 'value']):
            continue

        # Check constraint
        valid = cell['field'].test_value(cell['value'], constraints=['required'])
        if cell['field'].descriptor.get('primaryKey'):
            valid = valid and cell['field'].cast_value(cell['value']) is not None

        # Skip if valid
        if valid:
            continue

        # Add error

        error = Error(
            'required-constraint',
            cell,
            row_number
        )
        errors.append(error)

        # Remove cell
        cells.remove(cell)

    return errors
