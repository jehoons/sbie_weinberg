# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************

from sbie_weinberg.module.dream2015 import predictor 


def test_predictor():

    inpfile = 'code-with-inputdata/26input.CSV'
    # outfile = '/data/ui_output/dream/THERAPY_USER_PRED.CSV'

    predictor.run(inpfile, 'untracked_output.csv') 


