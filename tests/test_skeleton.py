#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from driving_data.skeleton import fib

__author__ = "atarla"
__copyright__ = "atarla"
__license__ = "mit"


def test_fib():
    # some assert tests
    with pytest.raises(AssertionError):
        fib('')
