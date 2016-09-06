# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import sys
if __name__ == '__main__':
    sys.path.append('../../..')
    pass

import hashlib 

import os, cPickle as pickle, re, json, pandas as pd, numpy as np

from sets import Set
from multiprocessing import Pool
from os.path import exists, split as pathsplit, join
from pdb import set_trace

from pydream2015 import rlang 
from pydream2015.rlang import glmnet, ch1scoring_fc
from pydream2015.util import update_progress, expand_poly2 
from pydream2015.feature import collect_feature 

import pydream2015, pytest, tempfile, time 

#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
from itertools import combinations, combinations_with_replacement 

from pydream2015.postproc import post_process

import shutil
from sets import Set

indir = join(pathsplit(pydream2015.__file__)[0], 'test_input')
outdir = join(pathsplit(pydream2015.__file__)[0], 'test_output')
indir = os.path.abspath(indir)
outdir = os.path.abspath(outdir)
pydream2015.initdatapath(indir, outdir)


def test_makedatasets():

    traintest_div('traintest_div.json') 

    pass


def traintest_div(outputfile):

    traintest_list = []
    
    for i in range(30): 

        # trainids, testids = pydream2015.util.divide_combi(ratio=0.25) 
        trainids, testids = pydream2015.util.divide(ratio=0.25)

        thisdataset = { 'train': trainids, 'test': testids, 'type': 'normal'}
        traintest_list.append(thisdataset) 

    trainids, testids = pydream2015.util.divide_train_leaderboard() 
    thisdataset = { 'train': trainids, 'test': testids, 'type': 'leaderboard' }
    traintest_list.append(thisdataset) 

    json.dump({'traintest_list': traintest_list}, open(outputfile, 'wb'), 
            separators=(',', ':'), sort_keys=True, indent=2)

    pass

