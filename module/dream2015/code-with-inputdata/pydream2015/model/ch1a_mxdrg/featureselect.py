# -*- coding: utf-8 -*-
#!/usr/bin/python 
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

codelist = ['GE', 'CN', 'ME', 'SM', 'DC', 'DE', 'DR']

SELECTED_RANDOMEFFECT = 'COMBINATION_ID'

def batchunit(inpfile, outfile, with_small=False, overwrite=False):

    jsonstr = open(inpfile).readlines()
    jsonstr = "\n".join(jsonstr)

    hash_object = hashlib.md5(jsonstr.encode())
    _cwd = os.getcwd()
    inpfile = join(_cwd, inpfile) 
    outfile = join(_cwd, outfile) 
    workdir = join('datafiles', hash_object.hexdigest()) 

    if not exists(workdir):
        os.makedirs(workdir) 

    os.chdir(workdir)
    mixedmodelmain(inpfile, outfile, with_small, overwrite) 


def mixedmodelmain(inpfile, outfile, with_small=False, overwrite=False):

    if exists(outfile) and (overwrite==False):
        return 

    config = json.load(open(inpfile)) 

    s1coef = config['s1coef']
    s1reff = config['s1reff']
    s1alp = config['s1alp']
    
    s2coef = config['s2coef']
    s2reff = config['s2reff']
    s2alp = config['s2alp']

    # STEP 1.  
    s1lbl = 'STEP1' 
    mixedmodel(codelist, s1lbl, coefmode='coef(%s)'%s1coef, with_small=with_small, 
            polyexp=False, selected_coefs=[], overwrite=overwrite, 
            with_randomeffect=s1reff, alpha=s1alp, ncores=1, clear=True,
            nrepeats=0)

    # STEP 2. 
    mfile = s1lbl + '.json'
    mdata = json.load(open(mfile, 'rb'))
    coefs = mdata['data']['coef(min)'].keys()

    s2lbl = 'STEP2' 
    mixedmodel(codelist, s2lbl, coefmode='coef(%s)' % s2coef, 
            with_small=with_small, polyexp=True, selected_coefs=coefs, 
            overwrite=overwrite, with_randomeffect=s2reff, alpha=s2alp,
            ncores=1, clear=True, nrepeats=0) 

    obsfile = s2lbl + '_OBSERV.csv' 
    predfile = s2lbl + '_PRED.csv'
    predleaderfile = s2lbl + '_PREDL.csv' 
    predleaderfile2 = s2lbl + '_PREDL2.csv' 
    confidfile = s2lbl + '_CONFID.csv'
    priofile = s2lbl + '_PRIO.csv'
    scorefile = s2lbl + '_SCORE.json'

    post_process(obsfile, predfile, predleaderfile, confidfile,
            priofile, predleaderfile2, scorefile, overwrite=overwrite)

    model = json.load(open(s2lbl+'.json'))
    coefnames = model['data']['coef(%s)'%s2coef].keys()
    coefnames.remove('(Intercept)')
    num_coefs = len(coefnames) 
    coefnames_all = ("*".join(coefnames)).split('*')
    num_coefsall = len(coefnames_all) 

    scoredata = json.load(open(scorefile))
    scoredata['workdir'] = os.getcwd()
    scoredata['config'] = config
    scoredata['model'] = {
            'shortly':{}, 
            'info':{},
            }
    scoredata['model']['shortly']['num_coefs'] = num_coefs
    scoredata['model']['shortly']['num_coefsall'] = num_coefsall
    scoredata['model']['shortly']['coefs'] = ",".join(coefnames)
    scoredata['model']['shortly']['coefsall'] = ",".join(coefnames_all)
    scoredata['model']['info'] = model 
    
    json.dump(scoredata, open(scorefile, 'wb'), separators=(',',':'), 
            sort_keys=True, indent=2) 

    shutil.copyfile(scorefile, outfile)


def mixedmodel(feature_codes, label, coefmode='coef(min)', polyexp=False,
        selected_coefs=[], with_small=False, overwrite=False, 
        train_ratio=0.7, nfolds=5, nrepeats=0, threshold=1000,
        with_randomeffect=False, alpha=1.0, ncores=1, clear=False):

    model_json = label + '.json'
    xDatafileTrain = label + '_xData.csv'
    yDatafile = label + '_yData.csv'
    xDatafileAns = label + '_xDataAns.csv'
    predfile = label + '_PRED.csv'
    predfileAns = label + '_PREDL.csv' 

    obsfile = label + '_OBSERV.csv'

    if exists(obsfile) and (overwrite==False):
        return 

    therapyfileTrain = pydream2015.DATA_COMBITHERAPY 
    dfTherapy = pd.read_csv(therapyfileTrain)

    therapyfileAns = pydream2015.DATA_COMBITHERAPY_LEADER

    features = []

    for code in feature_codes:
        features.append( feature_db[code] ) 
        pass

    # training data 준비하기 
    X = collect_feature(features, with_small=with_small, mode='train') 

    if polyexp and with_small: 
        selected_coefs = selected_coefs[0:5]
        pass

    if polyexp: 
        X = expand_poly2(X, cols=selected_coefs)
    else: 
        pass

    X.to_csv(xDatafileTrain, index=False)

    Xans = collect_feature(features, with_small=with_small, mode='leader') 
    
    if polyexp: 
        Xans = expand_poly2(Xans, cols=selected_coefs) 
    else:
        pass

    Xans.to_csv(xDatafileAns, index=False)

    print 'num_samples: %d, num_features: %d' % (X.shape[0], X.shape[1])

    if with_randomeffect:
        random_effect = {}
        random_effect['mean'] = {} 
        random_effect['std'] = {} 
        #therapy_groups = dfTherapy.groupby('CELL_LINE').groups
        therapy_groups = dfTherapy.groupby(SELECTED_RANDOMEFFECT).groups
        for cell in therapy_groups: 
            ids = therapy_groups[cell]
            syn_mean = dfTherapy.loc[ids,'SYNERGY_SCORE'].mean()
            syn_std = dfTherapy.loc[ids,'SYNERGY_SCORE'].std() 
            random_effect['mean'][cell] = syn_mean
            random_effect['std'][cell] = syn_std
            pass

        for i in dfTherapy.index:
            cell = dfTherapy.loc[i, SELECTED_RANDOMEFFECT] 
            dfTherapy.loc[i, 'SYNERGY_SCORE'] -= random_effect['mean'][cell]
            pass

    else:
        random_effect = None 
        pass
    
    y = dfTherapy[['SYNERGY_SCORE']]
    y.to_csv(yDatafile, index=False)

    model_training(xDatafileTrain, yDatafile, model_json, polyexp=False, 
            with_small=with_small, overwrite=overwrite, train_ratio=train_ratio, 
            nfolds=nfolds, nrepeats=nrepeats, threshold=threshold, 
            with_randomeffect=with_randomeffect, random_effect=random_effect,
            alpha=alpha,ncores=ncores)

    # test and scoring with training data set: 
    model_test(model_json, therapyfileTrain, xDatafileTrain, predfile, 
            coef_mode=coefmode, overwrite=overwrite)
    model_scoring(model_json, therapyfileTrain, obsfile, predfile, 
            coef_mode=coefmode)

    # answer with leaderboard data set: 
    model_test(model_json, therapyfileAns, xDatafileAns, predfileAns, coef_mode=coefmode, 
            overwrite=overwrite)

    if clear: 
        os.remove(xDatafileTrain)
        os.remove(xDatafileAns)
        pass



def model_scoring(model_json, therapyfile, obsfile, predfile,
        coef_mode='coef(min)'):

    dfTherapy = pd.read_csv(therapyfile) 

    dfObs = pd.DataFrame([])
    dfObs['CELL_LINE'] = dfTherapy['CELL_LINE']
    dfObs['COMBINATION_ID'] = dfTherapy['COMBINATION_ID']
    dfObs['OBSERVATION'] = dfTherapy['SYNERGY_SCORE']
    dfObs.to_csv(obsfile, index=False)

    # score 데이터를 modeldata에 누적시킨다. 
    __score_json = tempfile.mktemp() 
    ch1scoring_fc.run(obsfile, predfile, predfile, __score_json) 
    regress_data = json.load(open(model_json, 'rb')) 
    regress_data['data']['score(dream)'] = json.load(open(__score_json, 'rb'))
    regress_data['data']['score(dream)']['coef_mode'] = coef_mode

    json.dump(regress_data, open(model_json, 'wb'), separators=(',',':'), 
            sort_keys=True, indent=2) 


def model_training(xDatafile, yDatafile, model_json, polyexp=False, 
        with_small=False, overwrite=False, train_ratio=0.7, nfolds=5, 
        nrepeats=0, threshold=1000, with_randomeffect=False, 
        random_effect=None,alpha=1.0,ncores=1):

    if exists(model_json) and (overwrite==False):
        return 
    
    input_json = tempfile.mktemp()

    glmnet.make_input(os.path.abspath(xDatafile), 
            os.path.abspath(yDatafile), 
            input_json, 
            train_ratio=train_ratio, 
            nfolds=nfolds, 
            nrepeats=nrepeats, 
            figure=False, 
            normalize=True, 
            figurefile='__tmp_fig', 
            alpha=alpha,
            threshold=threshold,ncores=ncores)

    glmnet.run(input_json, model_json) 

    jsondata = json.load(open(model_json, 'rb'))
    jsondata['data']['randomeffect'] = random_effect

    json.dump(jsondata, open(model_json,'wb'), separators=(',',':'), 
            sort_keys=True, indent=2) 


def model_test(modeldata, therapyfile, therapyXfile, output_pred, 
        coef_mode='coef(min)', overwrite=False):

    if exists(output_pred) and (overwrite==False): 
        return 

    coefmode = coef_mode 
    
    regress_data = json.load(open(modeldata,'rb'))
    # rnd = regress_data['data']['random_effect']
    dfTherapy = pd.read_csv(therapyfile)

    dfX = pd.read_csv(therapyXfile)

    coef = regress_data['data'][coefmode]
    
    if regress_data['data']['randomeffect'] != None: 
        randeffect = regress_data['data']['randomeffect']['mean']
    else: 
        randeffect = None

    pred = __predict(dfTherapy, dfX, coef, randeffect) 

    crossvals = regress_data['data']['crossvals']

    dfPred = pd.DataFrame([]) 
    dfPred['CELL_LINE'] = dfTherapy['CELL_LINE']
    dfPred['COMBINATION_ID'] = dfTherapy['COMBINATION_ID']
    dfPred['PREDICTION'] = pred

    for i_cv in crossvals.keys():
        coef = crossvals[i_cv][coefmode]
        pred = __predict(dfTherapy, dfX, coef, randeffect)
        dfPred['CV_' + i_cv] = pred

    cvcols = ['CV_' + i_cv for i_cv in crossvals.keys()]
    for i in dfPred.index: 
        stdvalue = dfPred.loc[i, cvcols].std()
        dfPred.loc[i, 'CONFIDENCE'] = stdvalue

    dfPred['CONFIDENCE'] /= dfPred['CONFIDENCE'].max() 

    dfPred.to_csv(output_pred, index=False)


def small(name):
    return join(pathsplit(name)[0], 'small_' + pathsplit(name)[1])


def __predict(dfTherapy, dfX, coef, randeffect):

    coefnames = []
    coefvalues = []

    for c in coef.keys():
        if c == '(Intercept)':
            intercept = coef[c]
        else:
            coefnames.append(c) 
            coefvalues.append(coef[c]) 
    
    Xvalues = dfX[coefnames].values

    yhat = Xvalues.dot(np.array(coefvalues)) + intercept 

    if randeffect == None: 
        return yhat

    for i in dfTherapy.index:
        cell = dfTherapy.loc[i, SELECTED_RANDOMEFFECT]
        yhat[i] += randeffect[cell]

    return yhat 


if __name__ == '__main__':

    inpfile = sys.argv[1]
    outfile = sys.argv[2]

    batchunit(inpfile, outfile, with_small=False, overwrite=True)


