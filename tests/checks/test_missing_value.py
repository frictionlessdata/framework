# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from jsontableschema import Field
from goodtables.checks.missing_value import missing_value


# Check

def test_check_missing_value(log):
    errors = []
    cells = [
        {'number': 1,
         'header': 'name1',
         'value': 'value',
         'field': None},
        {'number': 2,
         'header': 'name2',
         'value': 'value',
         'field': None},
    ]
    missing_value(errors, cells, 1)
    assert log(errors) == []
    assert len(cells) == 2


def test_check_missing_value_problem(log):
    errors = []
    cells = [
        {'number': 1,
         'header': 'name1',
         'value': 'value',
         'field': None},
        {'number': 2,
         'header': 'name2',
         'field': None},
    ]
    missing_value(errors, cells, 1)
    assert log(errors) == [
        (1, 2, 'missing-value'),
    ]
    assert len(cells) == 1
