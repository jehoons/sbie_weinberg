
# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************

import sys 
sys.path.append('/home/pbs')
import pytest 
import glob
from os.path import join,dirname
import pandas as pd
from sbie_weinberg.module.dream2015 import predictor 
from ipdb import set_trace
import tempfile 
import os 


if __name__ == '__main__': 
    inputfile = sys.argv[1] 
    outputfile = sys.argv[2] 
    tmpdir = tempfile.mkdtemp() 
    cwd = os.getcwd() 
    os.chdir(tmpdir) 
    predictor.run_csv(join(cwd, inputfile), join(cwd, outputfile), repeat=100, sigma=0.05) 

