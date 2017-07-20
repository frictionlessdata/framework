# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from jsontableschema import Field
from goodtables.checks.extra_value import extra_value


# Test

def test_check_extra_value(log):
    errors = []
    columns = [
        {'number': 1,
         'header': 'name1',
         'value': 'value',
         'field': None},
        {'number': 2,
         'header': 'name2',
         'value': 'value',
         'field': None},
    ]
    extra_value(errors, columns, 1)
    assert log(errors) == []
    assert len(columns) == 2


def test_check_extra_value_problem(log):
    errors = []
    columns = [
        {'number': 1,
         'header': 'name1',
         'value': 'value',
         'field': None},
        {'number': 2,
         'value': 'value'},
    ]
    extra_value(errors, columns, 1)
    assert log(errors) == [
        (1, 2, 'extra-value'),
    ]
    assert len(columns) == 1
