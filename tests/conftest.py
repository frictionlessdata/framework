# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import yaml
import pytest
import fnmatch


@pytest.fixture(scope='session')
def log():
    def fixture(struct):
        # Pack errors/report to tuples list log:
        # - format for errors: (row-number, column-number, code)
        # - format for report: (table-number, row-number, column-number, code)
        result = []
        def pack_error(error, table_number='skip'):
            error = [error['row-number'], error['column-number'], error['code']]
            if table_number != 'skip':
                error = [table_number] + error
            return tuple(error)
        if isinstance(struct, list):
            for error in struct:
                result.append(pack_error(error))
        if isinstance(struct, dict):
            for table_number, table in enumerate(struct['tables'], start=1):
                for error in table['errors']:
                    result.append(pack_error(error, table_number))
        return result
    return fixture


def pytest_generate_tests(metafunc):
    if 'scenario' in metafunc.fixturenames:
        scenarios = {}
        for root, dirnames, filenames in os.walk('tests/scenarios'):
            for filename in fnmatch.filter(filenames, '*.yml'):
                filepath = os.path.join(root, filename)
                scenarios.update(yaml.load(io.open(filepath, encoding='utf-8')) or {})
        params = []
        for name in sorted(scenarios):
            params.append([name, scenarios[name]])
        metafunc.parametrize('name, scenario', params)
