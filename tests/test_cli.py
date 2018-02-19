# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest.mock as mock
except ImportError:
    import mock
import json
import datapackage
from click.testing import CliRunner
import goodtables.cli


# Tests

def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(goodtables.cli.cli, ['--version'])
    assert result.exit_code == 0
    assert len(result.output.split('.')) == 3


@mock.patch('goodtables.validate', autospec=True)
def test_cli_infer_schema_enables_infer_fields(validate_mock):
    CliRunner().invoke(goodtables.cli.cli, ['--infer-schema', 'data.csv'])

    last_call_args = validate_mock.call_args
    assert last_call_args is not None
    assert last_call_args[-1].get('infer_schema')
    assert last_call_args[-1].get('infer_fields')


@mock.patch('goodtables.validate', autospec=True)
def test_cli_accepts_multiple_sources(validate_mock):
    sources = ['data1.csv', 'data2.csv']
    expected_sources = [{'source': source} for source in sources]

    CliRunner().invoke(goodtables.cli.cli, sources)

    last_call_args = validate_mock.call_args
    assert last_call_args is not None
    assert last_call_args[0][0] == expected_sources


def test_cli_init():
    resource_path = 'data/valid.csv'

    result = CliRunner().invoke(goodtables.cli.init, [resource_path])

    assert result.exit_code

    dp = datapackage.Package(json.loads(result.output), strict=True)
    resource = dp.resources[0]
    assert resource.descriptor['path'] == resource_path
    assert 'schema' in resource.descriptor
