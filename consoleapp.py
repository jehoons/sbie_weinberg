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
from sbie_weinberg.module.attractor.fumia import simulator as attr_simulator
from sbie_weinberg.module.sfa.sfa_fumia import simulator as sfa_simulator
from sbie_weinberg.module.dream2015 import predictor as dream2015_predictor

root_dir = dirname(__file__)


def test_main():
    
    output_dir = 'untracked'

    if not os.path.exists(output_dir): 
        print('output_dir is not exist!')
        print('run mkdir untrackted')
        assert False 

    # run attractor analysis    

    demo_input = 'dataset/demo/demoinput_0.json'
    outfile = 'untracked/attr_output.json'

    attr_simulator.run(demo_input, outfile)

    attr_simulator.summary(outfile)


    # run signal flow analysis

    # sfa_fumia.run('SP', 'COLO205', ['NUTLIN-3'], ['GFs'], 'untracked/sfa_output.json')

    # run machine learning analysis

    #ml_dream2015.run(join(root_dir, 'module/dream2015/code-with-inputdata', \
    #    '26input.CSV'), 'dream2015_output.csv')


if __name__ == '__main__':
    test_main()    


