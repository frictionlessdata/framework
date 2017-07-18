# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


# General

DEFAULT_ERROR_LIMIT = 1000
DEFAULT_TABLE_LIMIT = 10
DEFAULT_ROW_LIMIT = 1000

# Presets

PRESETS = [
    'goodtables.presets.table',
    'goodtables.presets.datapackage',
    'goodtables.presets.nested',
]

# Checks

CHECKS = [
    'goodtables.checks.blank_header',
    'goodtables.checks.duplicate_header',
    'goodtables.checks.non_matching_header',
    'goodtables.checks.extra_header',
    'goodtables.checks.missing_header',
    'goodtables.checks.blank_row',
    'goodtables.checks.duplicate_row',
    'goodtables.checks.extra_value',
    'goodtables.checks.missing_value',
    'goodtables.checks.required_constraint',
    'goodtables.checks.pattern_constraint',
    'goodtables.checks.non_castable_value',
    'goodtables.checks.unique_constraint',
    'goodtables.checks.enumerable_constraint',
    'goodtables.checks.minimum_constraint',
    'goodtables.checks.maximum_constraint',
    'goodtables.checks.minimum_length_constraint',
    'goodtables.checks.maximum_length_constraint',
]
