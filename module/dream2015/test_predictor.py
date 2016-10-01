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
from ipdb import set_trace
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

    inputdata = {
        "input": {"celltype":"NCI-H520", "drugs":["BCL2L1","PTK2"]}, 
        "parameters": {"sigma": 1.0, "repeat": 1000}
        }

    df = pd.DataFrame([], 
        columns='CELL_LINE,COMPOUND_A,COMPOUND_B,COMBINATION_ID'.split(','))

    for i in range(inputdata['parameters']['repeat']):        
        df.loc[i, 'CELL_LINE'] = inputdata['input']['celltype']
        df.loc[i, 'COMPOUND_A'] = inputdata['input']['drugs'][0]
        df.loc[i, 'COMPOUND_B'] = inputdata['input']['drugs'][1]
        df.loc[i, 'COMBINATION_ID'] = ".".join(inputdata['input']['drugs'])

    infile = tempfile.mktemp()
    outfile = tempfile.mktemp()

    df.to_csv('inputdata.csv', index=False)
    sigma = inputdata['parameters']['sigma']

    predictor.run_csv('inputdata.csv', 'outputdata.csv', sigma=sigma) 

    # predictor.run_scan('output.csv')

