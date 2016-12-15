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
dir_sfa = abspath(join(dirname(__file__), 'sfa/sfa'))
sys.path.append(dir_sfa)
import sfa
from sbie_weinberg.module.sfa.sfa_fumia import simulator as sfa_simulator
from sbie_weinberg.dataset import demo
import glob
from ipdb import set_trace

from sbie_weinberg.module.sfa.sfa_fumia import simulator_comb as sfa_simulator_comb

# set_trace()


if not exists(join(dirname(__file__), 'untracked')):
    os.mkdir(join(dirname(__file__), 'untracked'))

#
# def test_single_inputjson():
#     # 1회 시뮬레이션
#
#     inputjson = join(abspath(dirname(__file__)), 'test_input.json')
#     outputjson = join(abspath(dirname(__file__)), 'untracked_test_output.json')
#
#     sfa_simulator.run(inputjson, outputjson)
#
#     print ('output:', outputjson)
#
#
# def test_many_inputjson():
#     # 몇개의 약물, 세포주 조합에 대한 시뮬레이션
#
#     files = glob.glob(join(dirname(demo.__file__), 'demoinput_sfa_*.json'))
#     print('files: ', files)
#     for inputjson in files:
#         print ('input:', inputjson)
#         filename = basename(inputjson)
#         outputjson = join(abspath(dirname(__file__)), 'untracked',
#             'out_' + filename)
#         sfa_simulator.run(inputjson, outputjson)
#
#         print ('output:', outputjson)
#
#     assert True


def test_combination_with_two_nodes():
    # simulation with node perturbation
    outputjson = join(abspath(dirname(__file__)), 'untracked', 'test_result.json')
    inputs = [] #['GFs']  # Add node names to be activated
    targets = ['RAF', 'p53']
    sfa_simulator_comb.run(inputs, targets, outputjson)
    # pass
