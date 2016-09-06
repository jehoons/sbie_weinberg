# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import os, sys, cPickle as pickle, re, json, pandas as pd, numpy as np, pytest
import pydream2015

from sets import Set
from multiprocessing import Pool
from os.path import exists, split as pathsplit, join
from pdb import set_trace
from os.path import split,join

indir = join(split(pydream2015.__file__)[0], 'test_input')
outdir = join(split(pydream2015.__file__)[0], 'test_output')

pydream2015.initdatapath(indir, outdir)

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


def run(therapy_user, overwrite=False):

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
    match_doseresponsecoef(therapy_user, matcheduser_doseresponsecoef, 
            overwrite=overwrite)
    match_smoothed_drugeffect(therapy_user, smoothed_drugeffect_STRING,
            matcheduser_drugeffect, overwrite=overwrite)

    pass


def test_run():
    
    therapy_user = 'therapy_user.csv' 
    run(therapy_user, overwrite=True) 
    
    pass


