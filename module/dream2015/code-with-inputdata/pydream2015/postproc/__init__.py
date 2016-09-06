# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import os, sys, re, json, pandas as pd, numpy as np
import time 
from multiprocessing import Pool
from os.path import exists, split as pathsplit, join
from pdb import set_trace

import pydream2015
import pytest

from pydream2015 import rlang 
from pydream2015.rlang import glmnet
from pydream2015.rlang import ch1scoring_fc
from pydream2015.util import update_progress

from pydream2015.feature import collect_feature 

import tempfile

from itertools import combinations, combinations_with_replacement 

#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt

__all__ = []

indir = join(pathsplit(pydream2015.__file__)[0], 'test_input')
outdir = join(pathsplit(pydream2015.__file__)[0], 'test_output')

pydream2015.initdatapath(indir, outdir)


def test_post_process(with_small, overwrite): 
    from pydream2015.postproc import post_process 
    from pydream2015.rlang import ch1scoring_fc 

    # basic input files 
    predfile = 'testdata/pred.csv'
    predleaderfile = 'testdata/predl.csv'
    obsfile = 'testdata/observ.csv'

    # intermediate result 
    confidencefile = 'processed.csv'

    # for submittion 
    out_priorityfile = 'priority.csv'
    out_leaderboard_pred = 'prediction.csv'

    dreamscorefile = 'score.json'

    post_process(obsfile, predfile, predleaderfile, confidencefile,
            out_priorityfile, out_leaderboard_pred, dreamscorefile, overwrite=overwrite)

    scoredata = json.load(open(dreamscorefile, 'rb')) 

    print (scoredata['global_score']['score'], \
        scoredata['global_score']['final'], \
        coredata['global_score']['tiebreak'])


def post_process(obsfile, predfile, predleaderfile, confidencefile, out_priorityfile,
        out_leaderboard_pred, dreamscorefile, overwrite=False):

    infile_for_priority = predfile

    if exists(dreamscorefile) and (overwrite==False):
        print ('file already exists:', dreamscorefile)
        return 
    else: 
        print ('>>', confidencefile)

    pred_df = pd.read_csv(infile_for_priority)

    cvcols = [] 
    for col in pred_df.columns:
        if col.find('CV_') == 0:
            cvcols.append(col) 
        else:
            pass         
        
    for i in pred_df.index: 
        stdvalue = pred_df.loc[i, cvcols].std()
        meanvalue = pred_df.loc[i, cvcols].mean()
        pred_df.loc[i, 'STDDEV'] = stdvalue
        pred_df.loc[i, 'AMEAN'] = np.abs(meanvalue)

    pred_df['CONFIDENCE']  = 1/(pred_df['STDDEV'] / pred_df['AMEAN'])
    pred_df['CONFIDENCE'] /= pred_df['CONFIDENCE'].max() 

    pred_df.to_csv(confidencefile, index=False)

    grouped = pred_df.groupby('COMBINATION_ID')
    dfMeanCon = grouped['CONFIDENCE'].mean().to_frame()
    dfMeanCon.to_csv(out_priorityfile)

    dfleader_pred = pd.read_csv(predleaderfile)
    dfleader_pred = dfleader_pred[['CELL_LINE','COMBINATION_ID','PREDICTION']]
    dfleader_pred.to_csv(out_leaderboard_pred, index=False)

    obsdf = pd.read_csv(obsfile)
    obsdf['SYNERGY_SCORE'] = obsdf['OBSERVATION']
    obsdf.to_csv(obsfile, index=False)

    ch1scoring_fc.run2(obsfile, predfile, out_priorityfile, dreamscorefile,
            overwrite=overwrite)

    pass


