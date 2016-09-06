# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of {pydream2015}.
#*************************************************************************
import os, sys, re, json, pandas as pd, numpy as np
import time 
#from sets import Set
from multiprocessing import Pool
from os.path import exists, split as pathsplit, join
from pdb import set_trace
from itertools import combinations, combinations_with_replacement 
import pytest
from numpy.random import permutation
import pydream2015

__start_time = 0 

def update_progress(idx, max_idx, updates=1000, blocks=50):
    """ This function is used for display progress bar in console environment.

    This function can be used to display the progression of the for-loops. In
    that case, the function should be called inside the loop, and total number
    of iteration(max_idx) and current index(idx) of the loop should be given to
    the function.

    For example: 

        for i in range(0,100):
            update_progress(i, 100)
    
    This function can also be used to display the progress of normal function
    consists of several steps. 

    For example:

        def my_function_with_3steps(): 

            update_progress(0, 3+1)

            ... step 1 ...
            update_progress(1, 3+1)

            ... step 2 ... 
            update_progress(2, 3+1)

            ... step 3 ...
            update_progress(3, 3+1)


    Args: 
        idx: current index of the for-loop
        max_idx: total number of iterations

    """
    global __start_time 

    import sys
    
    idx += 1

    if idx == 1: 
        __start_time = time.time() 

    elapsed_time = time.time() - __start_time 

    avgtime = elapsed_time / idx; 
    remaintime = (max_idx - idx)*avgtime 

    if idx>max_idx: 
        idx = max_idx 

    # updates = 1000
    if max_idx < updates:
        updates = max_idx

    sys.stdout.flush() 
    # blocks = 50
    if idx % (max_idx/updates) == 0 or (idx == max_idx):
        p = float(idx)/float(max_idx) 
        s = '\r[%s] %.02f%% (%.01fs)' % ('#'*int(p*blocks), p*100.0, remaintime)
        sys.stdout.write(s)
        sys.stdout.flush() 

    if idx == max_idx:
        sys.stdout.write('\n')
        sys.stdout.flush()

@pytest.mark.skipif(True, reason="")
def test_update_progress():

    for i in range(0,5):
        update_progress(i,5)
        time.sleep(1)


def expand_poly2(Xdata, cols=[]):

    if len(cols)>0: 
        if '(Intercept)' in cols: 
            cols.remove('(Intercept)')

        Xdata = Xdata[cols]

    XdataPoly = pd.DataFrame([]) 

    for combi in combinations_with_replacement(Xdata.columns.tolist(), 2):
        a = combi[0]
        b = combi[1]
        label = '%s*%s' % (a, b)
        mul = Xdata[[a]].values * Xdata[[b]].values
        XdataPoly[label] = mul[:, 0] 

    XdataPoly = pd.merge(XdataPoly, Xdata, left_index=True,
            right_index=True, how='left') 

    return XdataPoly


def test_divide():
    sys.path.append('..')    
    import pydream2015
    indir = join(pathsplit(pydream2015.__file__)[0], 'test_input')
    outdir = join(pathsplit(pydream2015.__file__)[0], 'test_output')
    indir = os.path.abspath(indir)
    outdir = os.path.abspath(outdir)
    pydream2015.initdatapath(indir, outdir)
    trainids, testids = pydream2015.util.divide() 
    pass 


def divide(therapy_traindata=None, ratio=0.25):

    if therapy_traindata == None: 
        therapy_traindata = pd.read_csv(pydream2015.DATA_COMBITHERAPY)

    ids = therapy_traindata.index.values.tolist() 
    ids_permuted = permutation(ids).tolist()
    num_test = int( float(len(ids))*ratio ) 
    test_list = ids_permuted[0:num_test]
    train_list = ids_permuted[num_test:]
    assert len(ids) == len(test_list+train_list)
    return train_list, test_list


def divide_combi(therapy_traindata=None, ratio=0.25):
    # 콤비네이션별로 비율을 결정한다. 

    if therapy_traindata == None: 
        therapy_traindata = pd.read_csv(pydream2015.DATA_COMBITHERAPY)

    grouped = therapy_traindata.groupby('COMBINATION_ID')
    cellcounts = grouped['CELL_LINE'].count().to_frame()

    for i in cellcounts.index: 
        n = cellcounts.loc[i, 'CELL_LINE']
        if n < 5: 
            num_test = np.nan
        elif n >= 5: 
            num_test = int( float(n)*ratio ) 
        pass 
        cellcounts.loc[i, 'TEST'] = num_test

    cellcounts.sort('CELL_LINE',inplace=True)
    # cellcounts.to_csv('cellcounts.csv')

    grouped_combi = therapy_traindata.groupby('COMBINATION_ID').groups
    test_list = []; train_list = [] 
    for combi in grouped_combi.keys():
        ids = grouped_combi[combi] 
        ids_permuted = permutation(ids).tolist()
        num_samps = len(ids) 

        if num_samps == 1: 
            train_list += ids
        elif num_samps >= 5: 
            num_test = int( cellcounts.loc[combi, 'TEST'] ) 
            test_list += ids_permuted[0:num_test]
            train_list += ids_permuted[num_test:]
        else: 
            print (num_samps)
            assert False 
        pass 

    assert therapy_traindata.shape[0] == len(test_list+train_list)
    assert set(test_list+train_list) == \
        set(therapy_traindata.index.values.tolist())

    point_class = pd.DataFrame([], 
            index=therapy_traindata.index.values.tolist())

    point_class.loc[train_list, 'POINT_CLASS'] = 'train'
    point_class.loc[test_list, 'POINT_CLASS'] = 'test'

    # return point_class 
    return train_list, test_list


@pytest.mark.skipif(True, reason="")
def test_divide_combi():

    import pydream2015
    indir = join(pathsplit(pydream2015.__file__)[0], 'test_input')
    outdir = join(pathsplit(pydream2015.__file__)[0], 'test_output')
    indir = os.path.abspath(indir)
    outdir = os.path.abspath(outdir)
    pydream2015.initdatapath(indir, outdir)

    
    therapy_traindata = pd.read_csv(pydream2015.DATA_COMBITHERAPY)
    trainids, testids = pydream2015.util.divide_combi(therapy_traindata, ratio=0.3) 

    print (len(trainids))
    print (len(testids))

    pass


def divide_train_leaderboard(): 
    
    # 초기에 배포된 방식, 즉 trainset과 leaderboard셋을 분리하여 각각 train과
    # test로 사용한다. 
    therapy_traindata = pd.read_csv(pydream2015.DATA_COMBITHERAPY)
    grouped = therapy_traindata.groupby('MARK').groups
    
    trainids = grouped['TRAINSET']
    testids = grouped['LEADERBOARDSET']

    return trainids, testids 


@pytest.mark.skipif(True, reason="")
def test_divide_train_leaderboard(): 
    sys.path.append('..')    
    import pydream2015
    indir = join(pathsplit(pydream2015.__file__)[0], 'test_input')
    outdir = join(pathsplit(pydream2015.__file__)[0], 'test_output')
    indir = os.path.abspath(indir)
    outdir = os.path.abspath(outdir)
    pydream2015.initdatapath(indir, outdir)

    trainids, testids = pydream2015.util.divide_train_leaderboard()



