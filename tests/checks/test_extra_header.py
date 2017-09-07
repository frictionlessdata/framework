# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from tableschema import Field
from goodtables.checks.extra_header import ExtraHeader


# Check

def test_check_extra_header(log):
    errors = []
    cells = [
        {'number': 1,
         'header': 'name1',
         'field': Field({'name': 'name1'})},
        {'number': 2,
         'header': 'name2',
         'field': Field({'name': 'name2'})},
    ]
    sample = []
    extra_header = ExtraHeader()
    extra_header.check_headers(errors, cells, sample=sample)
    assert log(errors) == []
    assert len(cells) == 2


def test_check_extra_header_infer(log):
    errors = []
    cells = [
        {'number': 1,
         'header': 'name1',
         'field': Field({'name': 'name1'})},
        {'number': 2,
         'header': 'name2'},
    ]
    sample = []
    extra_header = ExtraHeader(infer_fields=True)
    extra_header.check_headers(errors, cells, sample=sample)
    assert log(errors) == []
    assert len(cells) == 2
    assert cells[1]['field'].name == 'name2'


def test_check_extra_header_problem(log):
    errors = []
    cells = [
        {'number': 1,
         'header': 'name1',
         'field': Field({'name': 'name1'})},
        {'number': 2,
         'header': 'name2'},
    ]
    sample = []
    extra_header = ExtraHeader()
    extra_header.check_headers(errors, cells, sample=sample)
    assert log(errors) == [
        (None, 2, 'extra-header'),
    ]
    assert len(cells) == 1
