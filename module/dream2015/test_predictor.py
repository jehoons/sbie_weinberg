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
from sbie_weinberg.dataset import demo 
import json 
from pdb import set_trace


@pytest.mark.skipif(True, reason="temporal")
def test_predictor():

    inpfile = 'code-with-inputdata/26input.CSV'
    # outfile = '/data/ui_output/dream/THERAPY_USER_PRED.CSV'

    predictor.run(inpfile, 'untracked_output.csv') 


def test_single_runJSON():
    
    import tempfile

    inputfile = join(dirname(demo.__file__), 'demoinput_25.json')

    outputjson = 'untracked_output.json'

    with open(inputfile,'r') as fobj:
        inputdata = json.load(fobj)
        celltype = inputdata['input']['celltype']
        drugs = inputdata['input']['drugs']

    """ only two drugs combination is supported by this module. """
    assert len(drugs) == 2

    csv_inputfile = tempfile.mktemp()

    with open(csv_inputfile, 'w') as fout: 
        fout.write('CELL_LINE,COMPOUND_A,COMPOUND_B,COMBINATION_ID\n')
        fout.write('%s,%s,%s,%s\n' % (celltype, drugs[0], drugs[1],".".join(drugs)))

    csv_outputfile = tempfile.mktemp()
    # csv_outputfile = 'untracked_output.csv'    
    predictor.run(csv_inputfile, csv_outputfile)

    dataframe = pd.read_csv(csv_outputfile)

    # #row of dataframe should be one. 
    assert dataframe.shape[0] == 1

    data = {'synergy': dataframe.loc[0, 'PREDICTION']} 

    with open(outputjson, 'w') as foutjson:
        json.dump(data, foutjson, indent=4, sort_keys=True, separators=(',', ':'))


