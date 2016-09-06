# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************

import sys 
import os
import pytest
from os.path import join,dirname,exists
from pdb import set_trace

if __name__ == '__main__':    
    sys.path.append(join(dirname(__file__),'..'))

import sbie_weinberg
from sbie_weinberg.module.attractor import fumia as attr_fumia
from sbie_weinberg.module.sfa import sfa_fumia
from sbie_weinberg.module.dream2015 import model as ml_dream2015

root_dir = dirname(__file__)


def test_main():
    
    # run attractor analysis

    infile = 'untracked/test_input.json'
    outfile = 'untracked/attr_output.json'

    attr_fumia.run(infile, outfile)
    attr_fumia.summary(outfile)


    # run signal flow analysis 

    sfa_fumia.run('SP', 'COLO205', ['NUTLIN-3'], ['GFs'], 'untracked/sfa_output.json')


    # run machine learning analysis 

    ml_dream2015.run(join(root_dir, 'module/dream2015/code-with-inputdata', \
        '26input.CSV'), 'dream2015_output.csv')


if __name__ == '__main__':
    test_main()    


