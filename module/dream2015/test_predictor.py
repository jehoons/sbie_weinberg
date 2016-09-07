# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************

import pytest 
import glob
from os.path import join,dirname
import pandas as pd
from sbie_weinberg.module.dream2015 import predictor 
# from sbie_weinberg.dataset import demo 
# import json 
from pdb import set_trace
import tempfile


@pytest.mark.skipif(True, reason="temporal")
def test_run_csv():

    """ run_csv function allows CSV input format, and outputs CSV output format
     data """

    inpfile = 'code-with-inputdata/26input.CSV'
    # outfile = '/data/ui_output/dream/THERAPY_USER_PRED.CSV'

    predictor.run_csv(inpfile, 'untracked_output.csv') 


#@pytest.mark.skipif(True, reason="temporal")
def test_run():

    """ run function allow JSON input format, and outputs JSON output format 
    data """
    predictor.run('input.json', 'output.json') 


