#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from driving_data.track_driving_hist import process_input

__author__ = "atarla"
__copyright__ = "atarla"
__license__ = "mit"


def test_driving_data():
    # test if file exists
    with pytest.raises(FileNotFoundError):
        process_input(' ')
