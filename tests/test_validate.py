# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import json
import pytest
from goodtables import validate


# Infer preset

def test_validate_infer_table(log):
    report = validate('data/invalid.csv')
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
    assert report['tables'][0]['schema'] == None


def test_validate_report_schema_infer_schema():
    report = validate('data/valid.csv', infer_schema=True)
    assert report['tables'][0]['schema'] == 'table-schema'
