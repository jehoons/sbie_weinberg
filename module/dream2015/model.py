# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************

import sys,hashlib,pdb,pytest,tempfile,time 
from os.path import exists, split as pathsplit, join, dirname
from pdb import set_trace
import os, re, json, pandas as pd, numpy as np
from itertools import combinations, combinations_with_replacement 
import shutil

sys.path.append(join(dirname(__file__), 'code-with-inputdata'))
import pydream2015
from pydream2015 import rlang 
from pydream2015.rlang import glmnet, ch1scoring_fc
from pydream2015.util import update_progress, expand_poly2 
from pydream2015.feature import collect_feature 
from pydream2015.postproc import post_process

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

# codelist = ['GE', 'CN', 'ME', 'SM', 'DC', 'DE', 'DR']
codelist = ['GE', 'CN', 'ME', 'SM', 'DC', 'DE']

KGROUP = 'DRUG_KGROUP:10'


def run(therapy_user, predfile, userid='undefined_uid'):

    match_user_run(therapy_user, overwrite=True) 

    mixedmodel(codelist, 'STEP3_FULL', predfile, [], [], 
        inputfilename=therapy_user, userid_=userid, with_small=False, 
        overwrite=True, nrepeats=1, alpha=1.0, online=True)


def mixedmodel(feature_codes, label, predfile = 'output_pred.csv', trainids=[], 
    testids=[], inputfilename='', userid_=0, coefmode='coef(min)', 
    with_small=False, overwrite=False, train_ratio=0.66, nfolds=10, nrepeats=1, 
    threshold=1000, alpha=1.0, ncores=1, clear=False, testfile=None, 
    online=False):

    dst_dir = '.'

    shutil.copy(pydream2015.DATA_COMBITHERAPY, join(dst_dir, 'THERAPY_TRAINSET.CSV'))

    shutil.copy(pydream2015.DATA_COMBITHERAPY_TEST, join(dst_dir, 'THERAPY_TESTSET.CSV'))

    # shutil.copy(pydream2015.DATA_COMBITHERAPY,
    #     '/data/ui_input/dream/'+str(userid_)+'THERAPY_TRAINSET.CSV') 

    # shutil.copy(pydream2015.DATA_COMBITHERAPY_TEST, 
    #     '/data/ui_input/dream/'+str(userid_)+'THERAPY_TESTSET.CSV') 

    with_randomeffect = True 

    model_json = label + '.json'

    if exists(model_json) and (overwrite==False) and online==False:
        return 

    xDatafileTrain = label + '_xDataTrain.csv'
    yDatafileTrain = label + '_yDataTrain.csv'

    xDatafileTest = label + '_xDataTest.csv'
    yDatafileTest = label + '_yDataTest.csv'

    xDatafileAns = label + '_xDataAns.csv'

    # predfile = label + '_PRED.csv'

    obsfile = label + '_OBSERV.csv'

    EXPERIMENT_DATA = pd.read_csv(join(dst_dir, 'THERAPY_TRAINSET.CSV' ))

    features = []
    for code in feature_codes:
        features.append( feature_db[code] ) 

    TRAIN_SET = EXPERIMENT_DATA

    rndeffval2 = calc_randomeffect2(TRAIN_SET) 

    model_json = join(dirname(__file__), 'code-with-inputdata', 'STEP3_FULL.json')
    # model_json = '/data/platform_scripts/models/dream2015/code-with-inputdata/STEP3_FULL.json'
    
    model3 = json.load(open(model_json))
    coefmin = model3['data']['coef(min)']

    coefnames = [] 
    for coef in coefmin.keys(): 
        coefnames += coef.split('*')
   
    coefnames = set(coefnames)
    coefnames = list(coefnames) 
    linear_features = coefnames 
    all_coefnames_i = coefmin.keys()

    XTEST = collect_feature(features, with_small=with_small, mode='user') 

    fea_set = set(linear_features)
    xtest_set = set(XTEST.columns.values.tolist()) 
    fea_set = fea_set.intersection(xtest_set) 
    linear_features = list(fea_set) 

    XTEST = expand_poly2(XTEST, cols=linear_features) 

    set1 = set(all_coefnames_i)
    set2 = set(XTEST.columns.values.tolist())
    set1 = set1.intersection(set2) 

    XTEST = XTEST[list(set1)]

    TEST_SET = pd.read_csv(inputfilename)
    PREDICTION = TEST_SET.copy() 
    PREDICTION['SYNERGY_SCORE'] = np.nan
    Yprediction = predict(PREDICTION, XTEST, coefmin, rndeffval2) 
    PREDICTION['PREDICTION'] = Yprediction
    PREDICTION[['CELL_LINE','COMBINATION_ID','PREDICTION']].to_csv( \
            predfile, index=False)

    
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

    rndeff_monodrug = {'mean':{}, 'std':{}, 'points':{}} 
    groups_drug_a = therapyAll.groupby('COMPOUND_A').groups
    groups_drug_b = therapyAll.groupby('COMPOUND_B').groups
    
    drugs = [ee for ee in groups_drug_a.keys()] + \
        [ee for ee in groups_drug_b.keys()]

    # drugs = groups_drug_a.keys() + groups_drug_b.keys() 
    
    druggroups = {} 
    for drug in drugs:
        ids_a = []; ids_b = []
        # if groups_drug_a.has_key(drug):
        if drug in groups_drug_a: 
            ids_a = groups_drug_a[drug]

        # if groups_drug_b.has_key(drug): 
        if drug in groups_drug_b:
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

    rndeff = {
            'COMBINATION_ID': rndeff_combination_id, 
            'CELL_LINE': rndeff_cell_line, 
            # 'TISSUE': rndeff_tissue, 
            # 'KGROUP': rndeff_kgroup, 
            # 'KGROUP_TISSUE_ID': rndeff_kdrug_tissue_id, 
            'DRUG': rndeff_monodrug, 
            }

    return rndeff


def estimate_rndeff(rndeff, seriesdata):

    # combi_id = seriesdata['COMBINATION_ID']
    cell = seriesdata['CELL_LINE']
    drug_a = seriesdata['COMPOUND_A']
    drug_b = seriesdata['COMPOUND_B']

    mu_drug_a = 0; n_drug_a = 0
    mu_drug_b = 0; n_drug_b = 0
    mu_cell = 0; n_cell = 0

    # if rndeff['CELL_LINE']['mean'].has_key(cell): 
    if cell in rndeff['CELL_LINE']['mean']:
        mu_cell = rndeff['CELL_LINE']['mean'][cell]
        n_cell = rndeff['CELL_LINE']['points'][cell]

    # if rndeff['DRUG']['mean'].has_key(drug_a): 
    if drug_a in rndeff['DRUG']['mean']:
        mu_drug_a = rndeff['DRUG']['mean'][drug_a]
        n_drug_a = rndeff['DRUG']['points'][drug_a]

    # if rndeff['DRUG']['mean'].has_key(drug_b): 
    if drug_b in rndeff['DRUG']['mean']:
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

    coef['(Intercept)'] = coef0['(Intercept)']

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

    for k, i in enumerate(dfTherapy.index): 
        a_series = dfTherapy.loc[i] 
        yhat[k] += estimate_rndeff(randeffect, a_series)

    return yhat 


def update_therapy_data_with_kdrug(therapyfile, KGROUP):

    druggoups_df = pd.read_csv('druggroups.csv', index_col='Unnamed: 0') 

    newcolname = {}
    
    for col in druggoups_df.columns.values.tolist(): 
        newcolname[col] = 'DRUG_KGROUP:' + col

    # KGROUP = 'DRUG_KGROUP:10'
    druggoups_df.rename(columns=newcolname, inplace=True)
    
    therapy_df = pd.read_csv(therapyfile) 
    
    cellinfo_df = pd.read_csv(pydream2015.DATA_CELLINFO)
    
    therapy_merged = pd.merge(therapy_df, cellinfo_df, left_on='CELL_LINE',
            right_on='Sanger.Name', how='left')
    
    therapy_merged = pd.merge(therapy_merged, druggoups_df[[KGROUP]],
            left_on='COMBINATION_ID', right_index=True, how='left')

    for i in therapy_merged.index:
        drug_id = therapy_merged.loc[i, KGROUP] 
        tissue_id = therapy_merged.loc[i, 'Tissue..General.']
        therapy_merged.loc[i, 'KDRUG_TISSUE_ID'] = 'DC%d.%s' % (drug_id, tissue_id)

    therapy_merged.to_csv(therapyfile, index=False) 


# therapy_user = pydream2015.DATA_COMBITHERAPY_USER
gexdata = pydream2015.MYDATA_GENEEXPR_FILLED 
mutdata = pydream2015.DATA_MUTATION 
dd3dc = pydream2015.MYDATA_DRUG_DESC_3D_CONV
smoothed_CNV_STRING = pydream2015.MYDATA_SMOOTHED_CNV_STRING
smoothed_methyl_STRING = pydream2015.MYDATA_SMOOTHED_METHYL_STRING
smoothed_mut_STRING = pydream2015.MYDATA_SMOOTHED_MUTATION_STRING
smoothed_drugeffect_STRING = pydream2015.MYDATA_SMOOTHED_DRUGEFFECT_STRING

# userdata
matcheduser_gex = pydream2015.MYDATA_MATCHEDUSER_GEX 
matcheduser_mut = pydream2015.MYDATA_MATCHEDUSER_MUT
matcheduser_smoothed_CNV = pydream2015.MYDATA_MATCHEDUSER_SMOOTHED_CNV
matcheduser_smoothed_methyl = pydream2015.MYDATA_MATCHEDUSER_SMOOTHED_METHYL
matcheduser_smoothed_mut = pydream2015.MYDATA_MATCHEDUSER_SMOOTHED_MUT
matcheduser_dd3dc = pydream2015.MYDATA_MATCHEDUSER_DD3DC
matcheduser_drugeffect = pydream2015.MYDATA_MATCHEDUSER_DRUGEFFECT
matcheduser_doseresponsecoef = pydream2015.MYDATA_MATCHEDUSER_DRCC


def match_user_run(therapy_user, overwrite=False):

    from pydream2015.feature.match import match_gex
    from pydream2015.feature.match import match_mut
    from pydream2015.feature.match import match_dd3dc
    from pydream2015.feature.match import match_smoothed_mut_STRING
    from pydream2015.feature.match import match_smoothed_CNV 
    from pydream2015.feature.match import match_smoothed_methyl 
    from pydream2015.feature.match import match_doseresponsecoef 
    from pydream2015.feature.match import match_smoothed_drugeffect

    match_gex(therapy_user, gexdata, matcheduser_gex, overwrite=overwrite)
    
    match_mut(therapy_user, mutdata, matcheduser_mut, overwrite=overwrite) 
    
    match_dd3dc(therapy_user, dd3dc, matcheduser_dd3dc, overwrite=overwrite) 
    
    match_smoothed_mut_STRING(therapy_user, smoothed_mut_STRING,
            matcheduser_smoothed_mut, overwrite=overwrite) 
    
    match_smoothed_CNV(therapy_user, smoothed_CNV_STRING, matcheduser_smoothed_CNV,
            overwrite=overwrite) 
    
    match_smoothed_methyl(therapy_user, smoothed_methyl_STRING, 
            matcheduser_smoothed_methyl, overwrite=overwrite)
    
    #match_doseresponsecoef(therapy_user, matcheduser_doseresponsecoef, 
    #        overwrite=overwrite)
    
    match_smoothed_drugeffect(therapy_user, smoothed_drugeffect_STRING,
            matcheduser_drugeffect, overwrite=overwrite)


def test_predict():

    inpfile = 'code-with-inputdata/26input.CSV'
    # outfile = '/data/ui_output/dream/THERAPY_USER_PRED.CSV'

    outfile = 'outfile.csv'

    run('26input.csv', 'output.csv', userid='000') 

