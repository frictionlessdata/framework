# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from goodtables.checks.required_constraint import required_constraint


# Check

def test_check_required_constraint(log):
    errors = []
    cells = []
    required_constraint(errors, cells, 1)
    assert log(errors) == []
    assert len(cells) == 0
