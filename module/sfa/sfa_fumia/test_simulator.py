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
import pdb
import argparse
from os.path import abspath, join, dirname, basename, exists
import numpy as np
import pandas as pd
import pytest
import sys
dir_sfa = abspath(join(dirname(__file__), 'sfa'))
sys.path.append(dir_sfa)
import sfa
from sbie_weinberg.module.sfa.sfa_fumia import simulator as sfa_simulator
from sbie_weinberg.dataset import demo
import glob


if not exists(join(dirname(__file__), 'untracked')):
    os.mkdir(join(dirname(__file__), 'untracked'))


def test_single_inputjson():

    inputjson = join(abspath(dirname(__file__)), 'test_input.json')
    outputjson = join(abspath(dirname(__file__)), 'untracked/output.json')

    sfa_simulator.run(inputjson, outputjson)

    print ('output:', outputjson)

    assert True 

    
def test_many_inputjson():

    files = glob.glob(join(dirname(demo.__file__), 'demoinput*.json'))

    for inputjson in files:
        filename = basename(inputjson)
        outputjson = join(abspath(dirname(__file__)), 'untracked', 
            'out_' + filename)
        sfa_simulator.run(inputjson, outputjson)

        print ('output:', outputjson)

    assert True 


        
