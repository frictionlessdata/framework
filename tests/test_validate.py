# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import six
import json
import pytest
from pprint import pprint
from copy import deepcopy
from importlib import import_module
from goodtables import validate, init_datapackage


# Infer preset

def test_validate_infer_table(log):
    report = validate('data/invalid.csv')
    # will report missing value error for cell that does not have a header
    assert report['error-count'] == 7


def test_validate_infer_datapackage_path(log):
    report = validate('data/datapackages/invalid/datapackage.json')
    assert report['error-count'] == 2


def test_validate_infer_datapackage_dict(log):
    with open('data/datapackages/invalid/datapackage.json') as file:
        report = validate(json.load(file))
        assert report['error-count'] == 2


def test_validate_infer_nested(log):
    report = validate([{'source': 'data/invalid.csv'}])
    # will report missing value error for cell that does not have a header
    assert report['error-count'] == 7


# Report's preset

def test_validate_report_scheme_format_encoding():
    report = validate('data/valid.csv')
    assert report['preset'] == 'table'


# Report's scheme/format/encoding

def test_validate_report_scheme_format_encoding():
    report = validate('data/valid.csv')
    assert report['tables'][0]['scheme'] == 'file'
    assert report['tables'][0]['format'] == 'csv'
    assert report['tables'][0]['encoding'] == 'utf-8'


# Report's schema

def test_validate_report_schema():
    report = validate('data/valid.csv')
    assert report['tables'][0].get('schema') is None


def test_validate_report_schema_infer_schema():
    report = validate('data/valid.csv', infer_schema=True)
    assert report['tables'][0]['schema'] == 'table-schema'


# Nested source with individual checks

def test_validate_nested_checks(log):
    source = [
        ['field'],
        ['value', 'value'],
        [''],
    ]
    report = validate([
        {'source': source, 'checks': ['extra-value']},
        {'source': source, 'checks': ['blank-row']}
    ])
    assert log(report) == [
        (1, 2, 2, 'extra-value'),
        (2, 3, None, 'blank-row'),
    ]


# Invalid table schema

# TODO: enable after
# https://github.com/frictionlessdata/goodtables-py/issues/304
@pytest.mark.skip
def test_validate_invalid_table_schema(log):
    source = [
        ['name', 'age'],
        ['Alex', '33'],
    ]
    schema = {'fields': [
        {'name': 'name'},
        {'name': 'age', 'type': 'bad'},
    ]}
    report = validate(source, schema=schema)
    assert log(report) == [
        (1, None, None, 'schema-error'),
    ]


# Datapackage with css dialect header false

def test_validate_datapackage_dialect_header_false(log):
    descriptor = {
        'resources': [
            {
                'name': 'name',
                'data': [
                    ['John', '22'],
                    ['Alex', '33'],
                    ['Paul', '44'],
                ],
                'schema': {
                    'fields': [
                        {'name': 'name'},
                        {'name': 'age', 'type': 'integer'},
                    ]
                },
                'dialect': {
                    'header': False,
                }
            }
        ]
    }
    report = validate(descriptor)
    assert log(report) == []


# Source as pathlib.Path

@pytest.mark.skipif(sys.version_info < (3, 4), reason='not supported')
def test_source_pathlib_path_table():
    pathlib = import_module('pathlib')
    report = validate(pathlib.Path('data/valid.csv'))
    assert report['table-count'] == 1
    assert report['valid']


@pytest.mark.skipif(sys.version_info < (3, 4), reason='not supported')
def test_source_pathlib_path_datapackage():
    pathlib = import_module('pathlib')
    report = validate(pathlib.Path('data/datapackages/valid/datapackage.json'))
    assert report['table-count'] == 2
    assert report['valid']


# Catch exceptions

def test_validate_catch_all_open_exceptions(log):
    report = validate('data/latin1.csv', encoding='utf-8')
    assert log(report) == [
        (1, None, None, 'source-error'),
    ]


def test_validate_catch_all_iter_exceptions(log):
    # Reducing sample size to get raise on iter, not on open
    report = validate([['h'], [1], 'bad'], sample_size=1)
    assert log(report) == [
        (1, None, None, 'source-error'),
    ]


# Warnings

def test_validate_warnings_no():
    source = 'data/datapackages/invalid/datapackage.json'
    report = validate(source, preset='datapackage')
    assert len(report['warnings']) == 0


def test_validate_warnings_bad_datapackage_json():
    source = 'data/invalid_json.json'
    report = validate(source, preset='datapackage')
    assert len(report['warnings']) == 1
    assert 'Unable to parse JSON' in report['warnings'][0]


def test_validate_warnings_table_limit():
    source = 'data/datapackages/invalid/datapackage.json'
    report = validate(source, preset='datapackage', table_limit=1)
    assert len(report['warnings']) == 1
    assert 'table(s) limit' in report['warnings'][0]


def test_validate_warnings_row_limit():
    source = 'data/datapackages/invalid/datapackage.json'
    report = validate(source, preset='datapackage', row_limit=1)
    assert len(report['warnings']) == 2
    assert 'row(s) limit' in report['warnings'][0]
    assert 'row(s) limit' in report['warnings'][1]


def test_validate_warnings_error_limit():
    source = 'data/datapackages/invalid/datapackage.json'
    report = validate(source, preset='datapackage', error_limit=1)
    assert len(report['warnings']) == 2
    assert 'error(s) limit' in report['warnings'][0]
    assert 'error(s) limit' in report['warnings'][1]


def test_validate_warnings_table_and_row_limit():
    source = 'data/datapackages/invalid/datapackage.json'
    report = validate(source, preset='datapackage', table_limit=1, row_limit=1)
    assert len(report['warnings']) == 2
    assert 'table(s) limit' in report['warnings'][0]
    assert 'row(s) limit' in report['warnings'][1]


def test_validate_warnings_table_and_error_limit():
    source = 'data/datapackages/invalid/datapackage.json'
    report = validate(source, preset='datapackage', table_limit=1, error_limit=1)
    assert len(report['warnings']) == 2
    assert 'table(s) limit' in report['warnings'][0]
    assert 'error(s) limit' in report['warnings'][1]


# Empty source

def test_validate_empty_source():
    report = validate('data/empty.csv')
    assert report['tables'][0]['row-count'] == 0
    assert report['tables'][0]['error-count'] == 0


# No headers source

def test_validate_no_headers():
    report = validate('data/invalid_no_headers.csv', headers=None)
    assert report['tables'][0]['row-count'] == 3
    # will report missing header since headers are none
    assert report['tables'][0]['error-count'] == 3
    assert report['tables'][0]['errors'][0]['code'] == 'blank-header'
    assert report['tables'][0]['errors'][1]['code'] == 'blank-header'
    assert report['tables'][0]['errors'][2]['code'] == 'extra-value'


# Init datapackage

def test_init_datapackage_is_correct():
    resources_paths = [
        'data/valid.csv',
        'data/sequential_value.csv',
    ]
    dp = init_datapackage(resources_paths)

    assert dp is not None
    assert dp.valid, dp.errors
    assert len(dp.resources) == 2

    actual_resources_paths = [res.descriptor['path'] for res in dp.resources]
    assert sorted(resources_paths) == sorted(actual_resources_paths)


# Issues

def test_composite_primary_key_unique_issue_215(log):
    descriptor = {
        'resources': [
            {
                'name': 'name',
                'data':  [
                    ['id1', 'id2'],
                    ['a', '1'],
                    ['a', '2'],
                ],
                'schema': {
                    'fields': [
                        {'name': 'id1'},
                        {'name': 'id2'},
                    ],
                    'primaryKey': ['id1', 'id2']
                }
            }
        ],
    }
    report = validate(descriptor)
    assert log(report) == []


def test_composite_primary_key_not_unique_issue_215(log):
    descriptor = {
        'resources': [
            {
                'name': 'name',
                'data':  [
                    ['id1', 'id2'],
                    ['a', '1'],
                    ['a', '1'],
                ],
                'schema': {
                    'fields': [
                        {'name': 'id1'},
                        {'name': 'id2'},
                    ],
                    'primaryKey': ['id1', 'id2']
                }
            }
        ],
    }
    report = validate(descriptor, skip_checks=['duplicate-row'])
    assert log(report) == [
        (1, 3, 1, 'unique-constraint'),
    ]


def test_validate_infer_fields_issue_223():
    source = [
        ['name1', 'name2'],
        ['123', 'abc'],
        ['456', 'def'],
        ['789', 'ghi'],
    ]
    schema = {
        'fields': [{'name': 'name1'}]
    }
    report = validate(source, schema=schema, infer_fields=True)
    assert report['valid']


def test_validate_infer_fields_issue_225():
    source = [
        ['name1', 'name2'],
        ['123', None],
        ['456', None],
        ['789', None],
    ]
    schema = {
        'fields': [{'name': 'name1'}]
    }
    report = validate(source, schema=schema, infer_fields=True)


    errors = set([error.get("code") for error in report.get("tables")[0].get("errors")])
    assert report is not None
    assert len(errors) is 1
    assert {"missing-value"} == errors
    assert ~report['valid']


def test_fix_issue_312_inspector_should_report_table_as_invalid(log):
    report = validate([{'source': 'data/invalid_fix_312.xlsx'}])
    assert log(report) == [
        (1, None, 3, 'blank-header'),
        (1, None, 4, 'duplicate-header'),
        (1, None, 5, 'blank-header'),
        (1, 2, 3, 'missing-value'),
        (1, 2, 4, 'missing-value'),
        (1, 2, 5, 'missing-value'),
        (1, 3, None, 'duplicate-row'),
        (1, 4, 3, 'missing-value'),
        (1, 4, 4, 'missing-value'),
        (1, 4, 5, 'missing-value'),
        (1, 5, None, 'blank-row'),
        (1, 6, 3, 'extra-value'),
        (1, 6, 5, 'extra-value'),
    ]


def test_validate_missing_local_file_raises_source_error_issue_315(log):
    report = validate([{'source': 'invalid'}])
    assert log(report) == [
        (1, None, None, 'io-error'),
    ]


def test_validate_datapackage_with_schema_issue_348(log):
    DESCRIPTOR = {
        'resources': [
            {
                'name': 'people',
                'data': [
                    ['id', 'name', 'surname'],
                    ['p1', 'Tom', 'Hanks'],
                    ['p2', 'Meryl', 'Streep']
                ],
                'schema': {
                    'fields': [
                        {'name': 'id', 'type': 'string'},
                        {'name': 'name', 'type': 'string'},
                        {'name': 'surname', 'type': 'string'},
                        {'name': 'dob', 'type': 'date'}
                    ]
                }
            }
        ]
    }
    report = validate(DESCRIPTOR, checks=['structure', 'schema'])
    assert log(report) == [
        (1, None, 4, 'missing-header'),
    ]


def test_validate_datapackage_with_schema_structure_only_issue_348(log):
    DESCRIPTOR = {
        'resources': [
            {
                'name': 'people',
                'data': [
                    ['id', 'name', 'surname'],
                    ['p1', 'Tom', 'Hanks'],
                    ['p2', 'Meryl', 'Streep']
                ],
                'schema': {
                    'fields': [
                        {'name': 'id', 'type': 'string'},
                        {'name': 'name', 'type': 'string'},
                        {'name': 'surname', 'type': 'string'},
                        {'name': 'dob', 'type': 'date'}
                    ]
                }
            }
        ]
    }
    report = validate(DESCRIPTOR, checks=['structure'])
    assert report['valid']


def test_validate_geopoint_required_constraint_issue_231(log):
    report = validate('data/datapackages/geopoint/datapackage.json')
    assert report['valid']


def test_validate_fails_with_wrong_encoding_issue_274(log):
    # For now, by default encoding is detected incorectly by chardet
    report = validate('data/encoding-274.csv', encoding='utf-8')
    assert report['valid']


def test_validate_invalid_table_schema_issue_304(log):
    source = [
        ['name', 'age'],
        ['Alex', '33'],
    ]
    schema = {'fields': [
        {'name': 'name'},
        {'name': 'age', 'type': 'bad'},
    ]}
    report = validate(source, schema=schema)
    assert not report['valid']


def test_validate_order_fields_issue_313(log):
    source = 'data/order_fields_313.xlsx'
    schema = {'fields': [
        { 'name': 'Column_1', 'type': 'string', },
        { 'name': 'Column_2', 'type': 'string', 'constraints': { 'required': True } },
        { 'name': 'Column_3', 'type': 'string' },
        { 'name': 'Column_4', 'type': 'string' },
        { 'name': 'Column_5', 'type': 'string' }
    ]}
    # For now, the "non-matching-header" check is required to order the fields
    checks = ['non-matching-header', 'required-constraint']
    report = validate(source, schema=schema, checks=checks, order_fields=True)
    assert report['valid']


def test_validate_number_test_issue_232(log):
    # We check here that it doesn't raise exceptions
    source = 'data/number_test/datapackage.json'
    report = validate(source)
    assert not report['valid']


def test_validate_inline_not_a_binary_issue_349(log):
    with open('data/valid.csv') as source:
        report = validate(source)
        error = report['tables'][0]['errors'][0]
        assert error['code'] == 'source-error'
        assert error['message'] == 'Only byte streams are supported.'


@pytest.mark.skipif(six.PY2, reason='only python3')
def test_validate_inline_no_format_issue_349(log):
    with open('data/valid.csv', 'rb') as source:
        report = validate(source)
        error = report['tables'][0]['errors'][0]
        assert error['code'] == 'format-error'
        assert error['message'] == 'Format "None" is not supported'
