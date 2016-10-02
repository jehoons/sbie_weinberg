# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************

from ipdb import set_trace
import glob 
import pandas as pd 
import sys 
sys.path.append('../../../..')
import sbie_weinberg 
from sbie_weinberg.util import progressbar 
from sbie_weinberg.module.dream2015 import combinations 


def map(input_data, blocksize):
    N = input_data.shape[0]
    k = 0
    df0_list = [] 

    for i in range(0, N, blocksize):
        progressbar.update(k, N/blocksize) 
        st = i 
        if i + blocksize >= N: 
            ed = N - 1

        else: 
            ed = i + blocksize - 1

        df0 = input_data.loc[st : ed]
        df0_list.append(df0.copy(deep=True))
        k+=1 

    return df0_list


def reduce(filename_ptn):
    files = glob.glob(filename_ptn)
    dflist = [] 

    for i, a_file in enumerate(files):
        progressbar.update(i, len(files)) 
        df = pd.read_csv(a_file)
        dflist.append(df.copy(deep=True))

    dfs = pd.concat(dflist, ignore_index=True)
    dflist2 = []  
    preds = ['PREDICTION%d'%i for i in range(100)]
    dfs['SIGMA'] = None 

    for i,predcol in enumerate(preds): 
        progressbar.update(i, len(preds)) 
        df0 = dfs[['CELL_LINE', 'COMBINATION_ID', 'SIGMA', predcol]]
        df0.rename(columns={predcol:'PREDICTION'}, inplace=True)
        dflist2.append(df0.copy(deep=True))
        
    dfs2 = pd.concat(dflist2, ignore_index=True)
    dfs2['SIGMA'] = 0.5 
    dfs2.sort_values(by=['CELL_LINE', 'COMBINATION_ID'], inplace=True)
    
    return dfs2 


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'run with arg: -map or -reduce'
        exit()

    arg = sys.argv[1]

    if arg == '-map':
        allinps = combinations.generate()
        parts = map(allinps, 1000)
        for i,a_part in enumerate(parts): 
            a_part.to_csv('INPUT_PART_%d.csv'%i, index=False)

    elif arg == '-reduce':
        data = reduce('OUTPUT_PART_*')
        data.to_csv('REDUCED.csv')

    else: 
        print 'run with arg: -map or -reduce'
