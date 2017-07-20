# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from goodtables.checks.minimum_length_constraint import minimum_length_constraint


# Test

def test_check_minimum_length_constraint(log):
    errors = []
    columns = []
    minimum_length_constraint(errors, columns, 1)
    assert log(errors) == []
    assert len(columns) == 0
