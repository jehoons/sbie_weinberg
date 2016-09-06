# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import glob
import numpy as np
from pdb import set_trace 
import json 
import pandas as pd 

files = glob.glob('score*.json')

summary = pd.DataFrame([])
for i, fl in enumerate(files):
    modeldata = json.load(open(fl))
    model_complexity = len(modeldata['model']['data']['coef(min)'])

    coefs = modeldata['model']['data']['coef(min)']
    coefs_names = coefs.keys() 
    coefs_names.remove('(Intercept)')

    L2 = 0 
    L1 = 0 
    for coef in coefs_names: 
        L2 += coefs[coef]**2
        L1 += np.abs( coefs[coef] ) 

    workdir = modeldata['workdir']

    summary.loc[i, 'model'] = fl
    #final_mean = modeldata['reduce']['final_mean']
    #final_std = modeldata['reduce']['final_std']
    summary.loc[i, 'complexity'] = model_complexity
    summary.loc[i, 'L1'] = L1
    summary.loc[i, 'L2'] = L2

    cvids = modeldata['cv'].keys() 
    cvids = [ int(k) for k in cvids]
    cvids = sorted(cvids) 
    for cvid in cvids:
        cv_final = modeldata['cv']['%d'%cvid]['final']
        summary.loc[i, 'cv%d'%cvid] = cv_final

cv = [ 'cv%d'%cvid for cvid in range(0,30) ]
cv_all = [ 'cv%d'%cvid for cvid in range(0,31) ]

summary['mu'] = summary[cv].mean(axis=1)
summary['mu_all'] = summary[cv_all].mean(axis=1)

summary['std'] = summary[cv].std(axis=1)
summary['std_all'] = summary[cv_all].std(axis=1)

summary['eps'] = 1 - summary['mu'] + summary['std']**2
summary['eps_all'] = 1 - summary['mu_all'] + summary['std_all']**2

summary.to_csv('summary.csv', index=False)
summary.groupby('complexity').mean().to_csv('summary_mean.csv', index=True)

#set_trace()

    

