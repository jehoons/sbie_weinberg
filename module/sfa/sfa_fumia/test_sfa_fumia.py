# -*- coding: utf-8 -*-
#*************************************************************************
"""
Created on Thu Aug 25 15:01:33 2016

@author: Je-Hoon Song, song.jehoon@gmail.com
"""
# This file is part of {sbie_weinberg}.
#*************************************************************************

import os
import re
import json
import argparse
from os.path import abspath, join, dirname
import numpy as np
import pandas as pd
import pytest

dir_sfa = abspath(join(dirname(__file__), 'sfa'))

import sys
sys.path.append(dir_sfa)
import sfa

import pdb


from sbie_weinberg.module.sfa import sfa_fumia
from sbie_weinberg.dataset import demo
import glob


def test_single_inputjson():

    inputjson = join(abspath(dirname(__file__)), 'test_input.json')
    outputjson = join(abspath(dirname(__file__)), 'untracked/output.json')

    sfa_fumia.run(inputjson, outputjson)

    print ('output:', outputjson)


# @pytest.mark.skipif(True, reason='no reason')
def test_many_inputjson():

    files = glob.glob(join(dirname(demo.__file__), 'demoinput*.json'))
    outputjson = join(abspath(dirname(__file__)), 'untracked/output.json')

    for inputjson in files: 
        sfa_fumia.run(inputjson, outputjson)
        print ('output:', outputjson)

    