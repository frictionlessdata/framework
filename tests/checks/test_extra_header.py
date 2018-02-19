# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from tableschema import Field
from goodtables.checks.extra_header import ExtraHeader
import goodtables.cells


# Check

def test_check_extra_header(log):
    cells = [
        goodtables.cells.create_cell('name1', field=Field({'name': 'name1'}), column_number=1),
        goodtables.cells.create_cell('name2', field=Field({'name': 'name2'}), column_number=2),
    ]
    sample = []
    extra_header = ExtraHeader()
    errors = extra_header.check_headers(cells, sample=sample)
    assert log(errors) == []
    assert len(cells) == 2


def test_check_extra_header_infer(log):
    cells = [
        goodtables.cells.create_cell('name1', field=Field({'name': 'name1'}), column_number=1),
        goodtables.cells.create_cell('name2', column_number=2),
    ]
    sample = []
    extra_header = ExtraHeader(infer_fields=True)
    errors = extra_header.check_headers(cells, sample=sample)
    assert log(errors) == []
    assert len(cells) == 2
    assert cells[1]['field'].name == 'name2'


def test_check_extra_header_infer_with_data(log):
    cells = [
        goodtables.cells.create_cell('name1', field=Field({'name': 'name1'}), column_number=1),
        goodtables.cells.create_cell('name2', column_number=2),
    ]
    sample = [
        ['123', 'abc'],
        ['456', 'def'],
        ['789', 'ghi'],
    ]
    extra_header = ExtraHeader(infer_fields=True)
    errors = extra_header.check_headers(cells, sample=sample)
    assert log(errors) == []
    assert len(cells) == 2
    assert cells[1]['field'].name == 'name2'
    assert cells[1]['field'].type == 'string'


def test_check_extra_header_infer_with_empty_data(log):
    cells = [
        goodtables.cells.create_cell('name1', field=Field({'name': 'name1'}), column_number=1),
        goodtables.cells.create_cell('name2', column_number=2),
    ]
    sample = [
        ['123', ''],
        ['456', ''],
        ['789', ''],
    ]
    extra_header = ExtraHeader(infer_fields=True)
    errors = extra_header.check_headers(cells, sample=sample)
    assert log(errors) == []
    assert len(cells) == 2
    assert cells[1]['field'].name == 'name2'
    assert cells[1]['field'].type == 'string'


def test_check_extra_header_problem(log):
    cells = [
        goodtables.cells.create_cell('name1', field=Field({'name': 'name1'}), column_number=1),
        goodtables.cells.create_cell('name2', column_number=2),
    ]
    sample = []
    extra_header = ExtraHeader()
    errors = extra_header.check_headers(cells, sample=sample)
    assert log(errors) == [
        (None, 2, 'extra-header'),
    ]
    assert len(cells) == 1
