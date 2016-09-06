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

from sets import Set
from multiprocessing import Pool
from os.path import exists, split as pathsplit, join
from pdb import set_trace

from pydream2015 import rlang 
from pydream2015.rlang import glmnet, ch1scoring_fc
from pydream2015.util import update_progress, expand_poly2 
from pydream2015.feature import collect_feature 

import hashlib 
import pydream2015, pytest, tempfile, time 
import os, cPickle as pickle, re, json, pandas as pd, numpy as np

from itertools import combinations, combinations_with_replacement 

from pydream2015.postproc import post_process

import shutil
from sets import Set

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

import feature_sets

# codelist = ['GE', 'CN', 'ME', 'SM', 'DC', 'DE', 'DR']
# codelist = ['CN', 'ME', 'SM', 'DC', 'DE', 'DR']
codelist = feature_sets.codelist

# KGROUP = 'DRUG_KGROUP:10'
#@pytest.mark.skipif(False, reason="")

def test_mxdrg_tr(with_small, overwrite): 

    with_small = True
    overwrite = True

    run_training('output0001.json', 'score0001.json', 'traintest_div.json', 
            with_small=with_small, overwrite=overwrite, alpha=1.0)

    pass


def run_training(inpfile, outfile, traintest_div, with_small=False, 
        overwrite=False, alpha=1.0):

    if exists(outfile) and (overwrite==False):
        return 

    inpfile = os.path.abspath(inpfile) 
    outfile = os.path.abspath(outfile) 

    _str = "\n".join(open(inpfile).readlines())
    hash_object = hashlib.md5(_str.encode())
    modeldata = json.load(open(inpfile)) 
    workdir = modeldata['workdir']

   
    workdir = join('datafiles', hash_object.hexdigest()) 
    if not exists(workdir):
        os.makedirs(workdir) 

    os.chdir(workdir)

    input_path = pathsplit(inpfile)[0]
    input_file = pathsplit(inpfile)[1].split('.')[0]

    datafile = join(input_path, input_file + '_data.tar.gz') 

    shutil.copy(datafile, '.')
    os.system('tar -xvf %s' % datafile)

    step1data = json.load(open('STEP1.json'))
    step2data = json.load(open('STEP2.json'))

    shutil.copy(join('../..', traintest_div), '.')

    shutil.copy(pydream2015.DATA_COMBITHERAPY, 'THERAPY_TRAINSET.CSV') 
    shutil.copy(pydream2015.DATA_COMBITHERAPY_TEST, 'THERAPY_TESTSET.CSV') 

    datasetdef = json.load(open(traintest_div))
    traintest_list = datasetdef['traintest_list']

    for cvid, cvdata in enumerate(traintest_list): 
        trainids = cvdata['train'] 
        testids = cvdata['test']
        mixedmodel(codelist, 'STEP3_%d' % cvid, trainids, testids, 
                with_small=with_small, overwrite=overwrite, nrepeats=1,
                alpha=alpha)

        pass

    # second, make best model trained with full experimental data 
    mixedmodel(codelist, 'STEP3_FULL', [], [], with_small=with_small, 
            overwrite=overwrite, nrepeats=1, alpha=alpha)

    # 마지막으로 CV데이터들을 요약정리한다. 
    cv_summary = { 
            'cv': { }, 
            'reduce':{ }, 
            'workdir': workdir, 
            'model': json.load(open('STEP3_FULL.json'))
            } 

    final_arr = []
    tiebreak_arr = [] 
    
    for cvid, cvdata in enumerate(traintest_list): 
        STEP3_CVDATA = json.load(open('STEP3_%d.json' % cvid))
        final = STEP3_CVDATA['data']['score(dream)']['global_score']['final']
        tie = STEP3_CVDATA['data']['score(dream)']['global_score']['tiebreak']
        score = STEP3_CVDATA['data']['score(dream)']['global_score']['score']
        cv_summary['cv'][cvid] = {'final': final, 'tiebreak': tie, 'score': 
                score }

        final_arr.append(final)
        tiebreak_arr.append(tie)

        pass

    cv_summary['reduce'] = {
            'final_mean': np.mean(final_arr), 
            'final_std': np.std(final_arr), 
            'tiebreak_mean': np.mean(tiebreak_arr), 
            'tiebreak_std': np.std(tiebreak_arr),
            }

    json.dump(cv_summary, open('STEP3_CVRES.json', 'wb'), separators=(',',':'), 
            sort_keys=True, indent=2) 

    shutil.copy('STEP3_CVRES.json', outfile)

    tgzdata = pathsplit(outfile)[1].split('.')[0]+'_data.tar.gz'
    os.system('tar -cvzf ../../%s *' % tgzdata)

    pass


def mixedmodel(feature_codes, label, trainids=[], testids=[], coefmode='coef(min)', 
        with_small=False, overwrite=False, train_ratio=0.66, nfolds=10, nrepeats=1, 
        threshold=1000, alpha=1.0, ncores=1, clear=False, testfile=None):

    with_randomeffect = True 
    model_json = label + '.json'

    if exists(model_json) and (overwrite==False):
        return 

    xDatafileTrain = label + '_xDataTrain.csv'
    yDatafileTrain = label + '_yDataTrain.csv'

    xDatafileTest = label + '_xDataTest.csv'
    yDatafileTest = label + '_yDataTest.csv'

    xDatafileAns = label + '_xDataAns.csv'

    predfile = label + '_PRED.csv'
    obsfile = label + '_OBSERV.csv'

    step1data = json.load(open('STEP1.json'))
    step2data = json.load(open('STEP2.json'))
    monocoef = step1data['data']['coef(min)'].keys() 
    combicoef = step2data['data']['coef(min)'].keys() 

    EXPERIMENT_DATA = pd.read_csv( 'THERAPY_TRAINSET.CSV' ) 

    features = []
    for code in feature_codes:
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
    all_coefnames = Set(monocoef + combicoef)
    all_coefnames_i = all_coefnames.intersection(Xcolumns) 
    X = X[list(all_coefnames_i)]

    if trainids == []: 
        X.to_csv(xDatafileTrain, index=False)
        TRAIN_SET = EXPERIMENT_DATA

    else: 
        X.loc[trainids].to_csv(xDatafileTrain, index=False)
        TRAIN_SET = EXPERIMENT_DATA.loc[trainids]
        TRAIN_SET.to_csv(label + '_cv_train.csv', index=False)

        TEST_SET = EXPERIMENT_DATA.loc[testids]
        TEST_SET.to_csv(label + '_cv_test.csv', index=False)
        TEST_SET[['CELL_LINE','COMBINATION_ID','SYNERGY_SCORE']].to_csv( 
                obsfile, index=False)
        pass

    rndeffval2 = calc_randomeffect2(TRAIN_SET) 

    # We eliminate random effect from SYNERGY_SCORE from experimental data.
    # Then, we use the normalized SYNERGY_SCORE in regression step. 
    Y_without_RndEffect = TRAIN_SET.copy()
    for i in Y_without_RndEffect.index:
        a_therapy = Y_without_RndEffect.loc[i] 
        Y_without_RndEffect.loc[i, 'SYNERGY_SCORE'] -= estimate_rndeff(\
                rndeffval2, a_therapy) 
        pass

    Y_without_RndEffect[['SYNERGY_SCORE']].to_csv(yDatafileTrain, index=False)

    # Now, we train the mixed quadratic model with prepared normalized data.
    model_training(xDatafileTrain, yDatafileTrain, model_json, 
            with_small=with_small, overwrite=overwrite, train_ratio=train_ratio, 
            nfolds=nfolds, nrepeats=nrepeats, threshold=threshold,
            random_effect=rndeffval2, alpha=alpha,ncores=ncores)

    model3 = json.load(open(model_json))
    coefmin = model3['data']['coef(min)']

    # Next, we apply the trained model to evaluate and answer. Evaluation and
    # answer are crossvalidation and test mode, respectively.
    if trainids == []:        
        # This is test mode (answering to the test data set). In this mode, we
        # use all of the data points to train the model. We can not evaluate
        # this model because we don't know the experimental result.

        # Collect features for test data set, and then expand it. 
        XTEST = collect_feature(features, with_small=with_small, mode='test') 
        XTEST = expand_poly2(XTEST, cols=linear_features) 
        XTEST = XTEST[list(all_coefnames_i)]

        # Prepare therapy data for answering. The therapy data provides
        # categorical variables for computing random effects.
        TEST_SET = pd.read_csv('THERAPY_TESTSET.CSV')
        PREDICTION = TEST_SET.copy() 
        PREDICTION['SYNERGY_SCORE'] = np.nan
        Yprediction = predict(PREDICTION, XTEST, coefmin, rndeffval2) 
        PREDICTION['PREDICTION'] = Yprediction
        PREDICTION[['CELL_LINE','COMBINATION_ID','PREDICTION']].to_csv( \
                predfile, index=False)

        # In addition, we use training dataset to predict it's SYNERGY_SCORE,
        # and the compare experimental and predicted SYNERGY_SCORE. With this
        # result, we can sure that out final anwering result will not have
        # numerical bugs.  
        PREDICTION2 = TRAIN_SET.copy() 
        PREDICTION2['SYNERGY_SCORE'] = np.nan
        Yprediction2 = predict(PREDICTION2, X, coefmin, rndeffval2) 
        PREDICTION2['PREDICTION'] = Yprediction2
        PREDICTION2[['CELL_LINE','COMBINATION_ID','PREDICTION']].to_csv( \
                label+'_PRED_CHECK.csv', index=False)
        TRAIN_SET[['CELL_LINE','COMBINATION_ID','SYNERGY_SCORE']].to_csv( 
                label+'_OBS_CHECK.csv', index=False)

        # We can calculate the score, but the score is not used to evaluate the
        # model. The score is only used to judge if there is numerical problem
        # or not. 
        scorefile = tempfile.mktemp() 
        ch1scoring_fc.run2a(label+'_OBS_CHECK.csv', label+'_PRED_CHECK.csv', 
                scorefile) 
        model3['data']['score(dream)_check'] = json.load(open(scorefile, 'rb'))
        json.dump(model3, open(model_json, 'wb'), separators=(',',':'), 
                sort_keys=True, indent=2)

    else:
        # This is crossvalidation mode. In this mode, we can evaluate the model.
        PREDICTION = TEST_SET.copy() 
        PREDICTION['SYNERGY_SCORE'] = np.nan
        Yprediction = predict(PREDICTION, X.loc[testids], coefmin, rndeffval2) 
        PREDICTION['PREDICTION'] = Yprediction
        PREDICTION[['CELL_LINE','COMBINATION_ID','PREDICTION']].to_csv(predfile,
                index=False)

        scorefile = tempfile.mktemp() 
        ch1scoring_fc.run2a(obsfile, predfile, scorefile) 
        model3['data']['score(dream)'] = json.load(open(scorefile, 'rb'))
        json.dump(model3, open(model_json, 'wb'), separators=(',',':'), 
                sort_keys=True, indent=2)

        pass


def calc_randomeffect2(therapyAll):
    
    rndeff_combination_id = {'mean':{}, 'std':{}, 'points':{}} 
    therapy_groups = therapyAll.groupby('COMBINATION_ID').groups
    for group_key in therapy_groups:
        ids = therapy_groups[group_key]
        syn_mean = therapyAll.loc[ids,'SYNERGY_SCORE'].mean()
        syn_std = therapyAll.loc[ids,'SYNERGY_SCORE'].std() 
        syn_count = therapyAll.loc[ids,'SYNERGY_SCORE'].count()
        rndeff_combination_id['mean'][group_key] = syn_mean
        rndeff_combination_id['std'][group_key] = syn_std
        rndeff_combination_id['points'][group_key] = syn_count
        pass

    rndeff_cell_line = {'mean':{}, 'std':{}, 'points':{}} 
    therapy_groups = therapyAll.groupby('CELL_LINE').groups
    for group_key in therapy_groups:
        ids = therapy_groups[group_key]
        syn_mean = therapyAll.loc[ids,'SYNERGY_SCORE'].mean()
        syn_std = therapyAll.loc[ids,'SYNERGY_SCORE'].std() 
        syn_count = therapyAll.loc[ids,'SYNERGY_SCORE'].count()
        rndeff_cell_line['mean'][group_key] = syn_mean
        rndeff_cell_line['std'][group_key] = syn_std
        rndeff_cell_line['points'][group_key] = syn_count
        pass

    rndeff_monodrug = {'mean':{}, 'std':{}, 'points':{}} 
    groups_drug_a = therapyAll.groupby('COMPOUND_A').groups
    groups_drug_b = therapyAll.groupby('COMPOUND_B').groups
    drugs = groups_drug_a.keys() + groups_drug_b.keys() 
    druggroups = {} 
    for drug in drugs:
        ids_a = []; ids_b = []
        if groups_drug_a.has_key(drug):
            ids_a = groups_drug_a[drug]
        if groups_drug_b.has_key(drug): 
            ids_b = groups_drug_b[drug] 
        druggroups[drug] = ids_a + ids_b

    for group_key in druggroups.keys(): 
        ids = druggroups[group_key]
        syn_mean = therapyAll.loc[ids,'SYNERGY_SCORE'].mean()
        syn_std = therapyAll.loc[ids,'SYNERGY_SCORE'].std() 
        syn_count = therapyAll.loc[ids,'SYNERGY_SCORE'].count()
        rndeff_monodrug['mean'][group_key] = syn_mean
        rndeff_monodrug['std'][group_key] = syn_std
        rndeff_monodrug['points'][group_key] = syn_count
        pass

    rndeff = {
            'COMBINATION_ID': rndeff_combination_id, 
            'CELL_LINE': rndeff_cell_line, 
            'DRUG': rndeff_monodrug, 
            }

    return rndeff


def estimate_rndeff(rndeff, seriesdata):

    cell = seriesdata['CELL_LINE']
    drug_a = seriesdata['COMPOUND_A']
    drug_b = seriesdata['COMPOUND_B']

    mu_drug_a = 0; n_drug_a = 0
    mu_drug_b = 0; n_drug_b = 0
    mu_cell = 0; n_cell = 0

    if rndeff['CELL_LINE']['mean'].has_key(cell): 
        mu_cell = rndeff['CELL_LINE']['mean'][cell]
        n_cell = rndeff['CELL_LINE']['points'][cell]

    if rndeff['DRUG']['mean'].has_key(drug_a): 
        mu_drug_a = rndeff['DRUG']['mean'][drug_a]
        n_drug_a = rndeff['DRUG']['points'][drug_a]

    if rndeff['DRUG']['mean'].has_key(drug_b): 
        mu_drug_b = rndeff['DRUG']['mean'][drug_b]
        n_drug_b = rndeff['DRUG']['points'][drug_b]

    return (n_cell*mu_cell + n_drug_a*mu_drug_a + \
            n_drug_b*mu_drug_b)/(n_cell + n_drug_a + n_drug_b)


def model_training(xDatafile, yDatafile, model_json, with_small=False, \
        overwrite=False, train_ratio=0.7, nfolds=5, nrepeats=1, \
        threshold=1000, random_effect=None,alpha=1.0,ncores=1):

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
    
    glmnet.run2(input_json, model_json) 
    
    if random_effect != None: 
        jsondata = json.load(open(model_json, 'rb'))
        jsondata['data']['randomeffect'] = random_effect
        json.dump(jsondata, open(model_json,'wb'), separators=(',',':'), 
                sort_keys=True, indent=2) 


def predict(dfTherapy, dfX, coef0, randeffect):

    coef = {} 
    for k in coef0.keys():
        if k in dfX.columns.values.tolist():
            coef[k] = coef0[k] 

            pass

        pass

    coef['(Intercept)'] = coef0['(Intercept)']

    coefnames = []
    coefvalues = []

    for c in coef.keys():
        if c == '(Intercept)':
            intercept = coef[c]

            pass
        else:
            coefnames.append(c) 
            coefvalues.append(coef[c]) 

            pass
    
    Xvalues = dfX[coefnames].values

    yhat = Xvalues.dot(np.array(coefvalues)) + intercept 

    if randeffect == None: 
        return yhat

    for k, i in enumerate(dfTherapy.index): 
        a_series = dfTherapy.loc[i] 
        yhat[k] += estimate_rndeff(randeffect, a_series)

    return yhat 


if __name__ == '__main__':

    inpfile = sys.argv[1]
    outfile = sys.argv[2]

    run_training(inpfile, outfile, 'traintest_div.json', with_small=False, 
            overwrite=True, alpha=1.0)

    pass

