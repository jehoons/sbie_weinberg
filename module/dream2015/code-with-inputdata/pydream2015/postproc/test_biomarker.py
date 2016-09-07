# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import glob
import os
from os.path import join, split as pathsplit
import json
from pdb import set_trace
import pandas as pd
from os.path import exists

import sys
sys.path.append('..')

import pydream2015

from pydream2015.util import update_progress, expand_poly2
from pydream2015.feature import collect_feature

from sets import Set

import numpy as np
from numpy import corrcoef

indir = join(pathsplit(pydream2015.__file__)[0], 'test_input')
outdir = join(pathsplit(pydream2015.__file__)[0], 'test_output')
indir = os.path.abspath(indir)
outdir = os.path.abspath(outdir)
pydream2015.initdatapath(indir, outdir)

feature_db = {
    'GE': pydream2015.MYDATA_MATCHED_GEX, 
    'MU': pydream2015.MYDATA_MATCHED_MUT, 
    'CN': pydream2015.MYDATA_MATCHED_SMOOTHED_CNV, 
    'ME': pydream2015.MYDATA_MATCHED_SMOOTHED_METHYL, 
    'SM': pydream2015.MYDATA_MATCHED_SMOOTHED_MUT, 
    'DC': pydream2015.MYDATA_MATCHED_DD3DC, 
    'DE': pydream2015.MYDATA_MATCHED_DRUGEFFECT, 
    'DR': pydream2015.MYDATA_MATCHED_DRCC
    }

datadir = '../model/ch1b_mxdrg'
filelist = glob.glob(join(datadir, 'score*.json'))
#filelist = glob.glob(join(datadir, 'score0001.json'))

best_dir = './best'


def get_type(coefname):

    return coefname.split('.')[0]


def test_extractglobalcoeff(with_small, overwrite, outputfile='globalcoeff.csv'):

    if exists(outputfile) and (overwrite==False):
        return 

    if with_small: 
        data_size = 10
    else: 
        data_size = len(filelist) 

    coefdf = pd.DataFrame([], columns=['mono', 'combi_1', 'combi_2', 'mono_type', \
            'combi_1_type', 'combi_2_type', 'value', 'model'])

    idx = 0 
    
    for k,f in enumerate(filelist):
        if (with_small==True) and (k > 10): 
            break 

        jsondata = json.load(open(f))
        coefdata = jsondata['model']['data']['coef(min)']
        coefdata_list = coefdata.keys()
        coefdata_list.remove('(Intercept)')
        # print coefdata_list
        #clist += coefdata_list
        for c in coefdata_list: 
            words = c.split('*')
            if len(words) == 1: 
                coefdf.loc[idx, 'mono'] = words[0]
                coefdf.loc[idx, 'mono_type'] = get_type(words[0])
            elif len(words) == 2: 
                coefdf.loc[idx, 'combi_1'] = words[0]
                coefdf.loc[idx, 'combi_2'] = words[1]
                coefdf.loc[idx, 'combi_1_type'] = get_type(words[0])
                coefdf.loc[idx, 'combi_2_type'] = get_type(words[1])
            else: 
                assert False 

            coefdf.loc[idx, 'value'] = coefdata[c]
            coefdf.loc[idx, 'model'] = f
            idx += 1

        update_progress(k, data_size)

    coefdf.to_csv(outputfile, index=False)


def test_analcoeff(with_small, overwrite, inputfile='globalcoeff.csv', outputfile='analcoeff.csv'):

    if exists(outputfile) and (overwrite==False):
        return 

    # monotonic coefficient analysis: 
    dfdata = pd.read_csv(inputfile) 

    dfdata2 = pd.DataFrame([], columns=['count', 'mean', 'std'])
    coefmean = dfdata.groupby('mono')['value'].mean()
    coefstd = dfdata.groupby('mono')['value'].std()
    coefcount = dfdata.groupby('mono')['value'].count()
    
    dfdata2['mean'] = coefmean
    dfdata2['std'] = coefstd
    dfdata2['count'] = coefcount

    dfdata2.to_csv(outputfile)

    dfdata3 = dfdata.groupby('mono_type')['model'].count()
    dfdata3.to_frame().to_csv('mono_type_count.csv')



def test_groupped_test(with_small, overwrite, outputfile='Xdata.csv'):

    if exists(outputfile) and (overwrite==False):
        return 

    global best_dir

    modelfile = join(best_dir, 'STEP3_CVRES.json')
    assert exists(modelfile) 

    modeldata = json.load(open(modelfile))
    coefdict = modeldata['model']['data']['coef(min)']
    coefs = coefdict.keys()
    coefs.remove('(Intercept)')
    monocoef = [] 

    for c in coefs: 
        words = c.split('*') 
        monocoef += words 

    print (monocoef)

    sys.path.append(datadir)
    import feature_sets 
    codelist = feature_sets.codelist 

    features = []
    for code in codelist:
        features.append( feature_db[code] ) 
        pass

    # Prepare training data
    X = collect_feature(features, with_small=with_small, mode='train') 

    Xcolumns = Set(X.columns.values.tolist())
    linear_features = list(Xcolumns.intersection(Set(monocoef))) 
    X = expand_poly2(X, cols=linear_features)

    # Now, Xcolumns containss quadratic terms. We also need extra codes for
    # matching 'small feature sets'.
    Xcolumns = Set(X.columns.values.tolist())
    #all_coefnames = Set(monocoef + combicoef)
    all_coefnames = Set(coefs)
    all_coefnames_i = all_coefnames.intersection(Xcolumns) 
    X = X[list(all_coefnames_i)]

    X.to_csv(outputfile) 


def test_groupped_analysis(with_small, overwrite, \
        outputfile='grouped_analysis.csv'):

    if exists(outputfile) and (overwrite==False):
        return 

    global best_dir

    survey_combi = pd.read_csv('survey_1b_combi.csv')

    X = pd.read_csv('Xdata.csv', index_col='Unnamed: 0')
    features = X.columns.values.tolist()

    Yp = pd.read_csv('best/STEP3_FULL_PRED_CHECK.csv')
    Yo = pd.read_csv('best/STEP3_FULL_OBS_CHECK.csv')

    assert X.shape[0] == Yp.shape[0] 
    assert X.shape[0] == Yo.shape[0] 

    DATA = pd.merge(X, Yo, left_index=True, right_index=True)
    DATA = pd.merge(DATA, Yp[['PREDICTION']], left_index=True, right_index=True)

    grouped = DATA.groupby('COMBINATION_ID').groups

    output_df = pd.DataFrame([], columns=['COMBINATION_ID', 'FEA_A_TYPE', \
            'FEA_B_TYPE', 'FEATURE_A', 'FEATURE_B', 'LABEL_A', 'LABEL_B', 'FEA_TYPE', \
            'PEARSONR', 'PEARSONR_ABS', 'Direction_feature', 'Direction_combo'])

    idx = 0 
    for k, combi in enumerate(survey_combi['COMBINATION_ID'].values):
        update_progress(k, survey_combi.shape[0])

        ids = grouped[combi]
        DATAgrouped = DATA.loc[ids]
        n_samp_grp = len(ids)
        
        for fea in features: 
            # print fea
            fea_values = DATAgrouped[fea].values.tolist()
            pred_values = DATAgrouped['PREDICTION'].values.tolist()
            
            assert n_samp_grp == len(fea_values)
            assert n_samp_grp == len(pred_values)
 
            words = fea.split('*')
            pearson_r = corrcoef(pred_values, fea_values)[0,1]

            #print fea_values 
            #print pred_values 
            #print pearson_r 

            output_df.loc[idx, 'COMBINATION_ID'] = combi 

            output_df.loc[idx, 'PEARSONR'] = pearson_r
            output_df.loc[idx, 'PEARSONR_ABS'] = np.abs(pearson_r)
            if len(words)==1:
                output_df.loc[idx, 'FEA_A_TYPE'] = get_type( words[0] ) 
                output_df.loc[idx, 'FEATURE_A'] = words[0]
                output_df.loc[idx, 'FEA_TYPE'] = 'linear'
                output_df.loc[idx, 'LABEL_A'] = words[0].split('.')[1]

            elif len(words)==2:
                output_df.loc[idx, 'FEA_A_TYPE'] = get_type( words[0] ) 
                output_df.loc[idx, 'FEA_B_TYPE'] = get_type( words[1] ) 
                output_df.loc[idx, 'FEATURE_A'] = words[0]
                output_df.loc[idx, 'FEATURE_B'] = words[1]
                output_df.loc[idx, 'FEA_TYPE'] = 'quadratic'
                output_df.loc[idx, 'LABEL_A'] = words[0].split('.')[1]
                output_df.loc[idx, 'LABEL_B'] = words[1].split('.')[1]

            else: 
                assert False

            # print corrval
            idx += 1

    # todo - 그룹으로 묶은후에 나머지 분석을 수행하도록 하자. 
    output_df.to_csv(outputfile, index=False)


def test_prepare_survey(with_small, overwrite, outputfile='grouped_analysis_v2.csv', 
        outputfile2='mean_abs_r.csv'):

    overwrite = True 

    if exists(outputfile) and (overwrite==False):
        return 

    # global best_dir
    df1 = pd.read_csv('grouped_analysis.csv')
    filtered = df1.loc[ (df1['PEARSONR_ABS']>0.1) & (df1['FEA_TYPE']=='linear')]

    filtered2 = filtered.sort_values(by=['COMBINATION_ID', 'PEARSONR'], ascending=False) 
    filtered2.to_csv(outputfile, index=False)

    filteredGrp = filtered2.groupby('COMBINATION_ID')
    mean_abs_r = filteredGrp['PEARSONR_ABS'].mean().to_frame() 
    mean_abs_r.to_csv(outputfile2) 

