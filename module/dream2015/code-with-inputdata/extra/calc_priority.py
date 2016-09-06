# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of {pydream2015}.
#*************************************************************************

# execution: 
# py.test -qs calc_priority.py

import sys
from sets import Set
from os.path import exists, split as pathsplit, join
from pdb import set_trace
import pytest, tempfile, time 
import os, cPickle as pickle
import json, pandas as pd, numpy as np
from sets import Set


def test_calc_priority():

    calc_priority('test_data') 


def calc_priority(workdir):

    import glob
    files = glob.glob(workdir+'/STEP3_*_OBSERV.csv')
    print 'CV size: %d' % len(files)
    # obs_all = pd.DataFrame
    for cvid in range(0, len(files)):
        obsfile = join(workdir, 'STEP3_%d_OBSERV.csv' % cvid) 
        predfile = join(workdir, 'STEP3_%d_PRED.csv' % cvid)
        if cvid == 0: 
            obs_df = pd.read_csv(obsfile)
            pred_df = pd.read_csv(predfile)
        else: 
            obs_1 = pd.read_csv(obsfile)
            pred_1 = pd.read_csv(predfile)
            obs_df = obs_df.append(obs_1, ignore_index=True)
            pred_df = pred_df.append(pred_1, ignore_index=True) 

            pass

        pass

    assert np.prod( obs_df['CELL_LINE'] == pred_df['CELL_LINE'] ) == 1
    assert np.prod( obs_df['COMBINATION_ID'] == pred_df['COMBINATION_ID'] ) == 1

    full_pred = pd.read_csv( join(workdir, 'STEP3_FULL_PRED.csv') ) 
    drug_ids_in_test = Set(full_pred['COMBINATION_ID'].values.tolist())
    drug_ids_in_test = list(drug_ids_in_test) 

    obs_df['PREDICTION'] = pred_df['PREDICTION']
    obs_df['ERROR'] = obs_df['SYNERGY_SCORE'] - obs_df['PREDICTION']
    obs_df['ERROR_NORM'] = obs_df['ERROR'] / obs_df['SYNERGY_SCORE']

    obs_df.to_csv('combination_priority_step1.csv', index=False)

    priority = obs_df.groupby('COMBINATION_ID')['ERROR_NORM'].std()
    priority = priority.to_frame()
    priority = priority.loc[drug_ids_in_test]
    
    priority['CONFIDENCE'] = 1 / priority['ERROR_NORM']
    priority['CONFIDENCE'] = priority['CONFIDENCE'] / \
            priority['CONFIDENCE'].max()

    priority.to_csv('combination_priority_step2.csv')

    priority[['CONFIDENCE']].to_csv('combination_priority.csv')
   
    #oldversion = pd.read_csv('combination_priority_oldversion.csv')
    #assert Set(priority.index.values.tolist()) == \
    #        Set(oldversion['COMBINATION_ID'].values.tolist()) 

    pass

