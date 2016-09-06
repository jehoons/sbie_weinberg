# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of {pydream2015}.
#*************************************************************************
import pytest

def pytest_addoption(parser):
    parser.addoption("--with_small", action="store_true", 
            help="Use small-scale data for quick test")

    parser.addoption("--overwrite", action="store_true", 
            help="Force overwriting existing results")


def pytest_generate_tests(metafunc):
    if 'with_small' in metafunc.fixturenames:
        if metafunc.config.option.with_small:
            with_small = True
        else: 
            with_small = False

        metafunc.parametrize("with_small", [with_small])

    if 'overwrite' in metafunc.fixturenames:
        if metafunc.config.option.overwrite:
            overwrite = True
        else: 
            overwrite = False

        metafunc.parametrize("overwrite", [overwrite])

