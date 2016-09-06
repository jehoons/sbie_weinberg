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

therapy = pydream2015.DATA_COMBITHERAPY

therapy_test = pydream2015.DATA_COMBITHERAPY_TEST

therapy_leader = pydream2015.DATA_COMBITHERAPY_LEADER

gexdata = pydream2015.MYDATA_GENEEXPR_FILLED 

mutdata = pydream2015.DATA_MUTATION 

dd3dc = pydream2015.MYDATA_DRUG_DESC_3D_CONV

smoothed_CNV_STRING = pydream2015.MYDATA_SMOOTHED_CNV_STRING

smoothed_methyl_STRING = pydream2015.MYDATA_SMOOTHED_METHYL_STRING

smoothed_mut_STRING = pydream2015.MYDATA_SMOOTHED_MUTATION_STRING

smoothed_drugeffect_STRING = pydream2015.MYDATA_SMOOTHED_DRUGEFFECT_STRING

# traindata: 
matched_gex = pydream2015.MYDATA_MATCHED_GEX 
matched_mut = pydream2015.MYDATA_MATCHED_MUT
matched_smoothed_CNV = pydream2015.MYDATA_MATCHED_SMOOTHED_CNV
matched_smoothed_methyl = pydream2015.MYDATA_MATCHED_SMOOTHED_METHYL
matched_smoothed_mut = pydream2015.MYDATA_MATCHED_SMOOTHED_MUT
matched_dd3dc = pydream2015.MYDATA_MATCHED_DD3DC
matched_drugeffect = pydream2015.MYDATA_MATCHED_DRUGEFFECT
matched_doseresponsecoef = pydream2015.MYDATA_MATCHED_DRCC

# test
matchedtest_gex = pydream2015.MYDATA_MATCHEDTEST_GEX 
matchedtest_mut = pydream2015.MYDATA_MATCHEDTEST_MUT
matchedtest_smoothed_CNV = pydream2015.MYDATA_MATCHEDTEST_SMOOTHED_CNV
matchedtest_smoothed_methyl = pydream2015.MYDATA_MATCHEDTEST_SMOOTHED_METHYL
matchedtest_smoothed_mut = pydream2015.MYDATA_MATCHEDTEST_SMOOTHED_MUT
matchedtest_dd3dc = pydream2015.MYDATA_MATCHEDTEST_DD3DC
matchedtest_drugeffect = pydream2015.MYDATA_MATCHEDTEST_DRUGEFFECT
matchedtest_doseresponsecoef = pydream2015.MYDATA_MATCHEDTEST_DRCC

# leaderboard
matchedleader_gex = pydream2015.MYDATA_MATCHEDLEADER_GEX 
matchedleader_mut = pydream2015.MYDATA_MATCHEDLEADER_MUT
matchedleader_smoothed_CNV = pydream2015.MYDATA_MATCHEDLEADER_SMOOTHED_CNV
matchedleader_smoothed_methyl = pydream2015.MYDATA_MATCHEDLEADER_SMOOTHED_METHYL
matchedleader_smoothed_mut = pydream2015.MYDATA_MATCHEDLEADER_SMOOTHED_MUT
matchedleader_dd3dc = pydream2015.MYDATA_MATCHEDLEADER_DD3DC
matchedleader_drugeffect = pydream2015.MYDATA_MATCHEDLEADER_DRUGEFFECT
matchedleader_doseresponsecoef = pydream2015.MYDATA_MATCHEDLEADER_DRCC


def test_match_gex(with_small, overwrite):
    from pydream2015.feature.match import match_gex
    match_gex(therapy, gexdata, matched_gex, overwrite=overwrite)
    match_gex(therapy_test, gexdata, matchedtest_gex, overwrite=overwrite)
    match_gex(therapy_leader, gexdata, matchedleader_gex, overwrite=overwrite)


def test_match_mut(with_small, overwrite):
    from pydream2015.feature.match import match_mut
    match_mut(therapy, mutdata, matched_mut, overwrite=overwrite) 
    match_mut(therapy_test, mutdata, matchedtest_mut, overwrite=overwrite) 
    match_mut(therapy_leader, mutdata, matchedleader_mut, overwrite=overwrite) 


def test_match_dd3d(with_small, overwrite):
    pass 


def test_match_dd3dc(with_small, overwrite):
    from pydream2015.feature.match import match_dd3dc
    match_dd3dc(therapy, dd3dc, matched_dd3dc, overwrite=overwrite) 
    match_dd3dc(therapy_test, dd3dc, matchedtest_dd3dc, overwrite=overwrite) 
    match_dd3dc(therapy_leader, dd3dc, matchedleader_dd3dc, overwrite=overwrite) 


#def test_match_smoothed_drugeffect_NCI():
#    # Not yet
#    pass 
#
#
#def test_match_smoothed_drugeffect_STRING():
#    # Not yet
#    pass 
#
#
#def test_match_smoothed_mut_NCI():
#    # Not yet
#    pass 
#

def test_match_smoothed_mut_STRING(with_small, overwrite):
    from pydream2015.feature.match import match_smoothed_mut_STRING
    match_smoothed_mut_STRING(therapy, smoothed_mut_STRING, 
            matched_smoothed_mut, overwrite=overwrite) 
    match_smoothed_mut_STRING(therapy_test, smoothed_mut_STRING, 
            matchedtest_smoothed_mut, overwrite=overwrite) 
    match_smoothed_mut_STRING(therapy_leader, smoothed_mut_STRING,
            matchedleader_smoothed_mut, overwrite=overwrite) 


def test_match_smoothed_CNV(with_small, overwrite):
    from pydream2015.feature.match import match_smoothed_CNV
    match_smoothed_CNV(therapy, smoothed_CNV_STRING, matched_smoothed_CNV,
            overwrite=overwrite) 
    match_smoothed_CNV(therapy_test, smoothed_CNV_STRING, matchedtest_smoothed_CNV,
            overwrite=overwrite) 
    match_smoothed_CNV(therapy_leader, smoothed_CNV_STRING, matchedleader_smoothed_CNV,
            overwrite=overwrite) 


def test_match_smoothed_methyl(with_small, overwrite):
    from pydream2015.feature.match import match_smoothed_methyl
    match_smoothed_methyl(therapy, smoothed_methyl_STRING, 
            matched_smoothed_methyl, overwrite=overwrite)
    match_smoothed_methyl(therapy_test, smoothed_methyl_STRING, 
            matchedtest_smoothed_methyl, overwrite=overwrite)
    match_smoothed_methyl(therapy_leader, smoothed_methyl_STRING, 
            matchedleader_smoothed_methyl, overwrite=overwrite)


def test_match_smoothed_drugeffect(with_small, overwrite):
    from pydream2015.feature.match import match_smoothed_drugeffect
    match_smoothed_drugeffect(therapy, smoothed_drugeffect_STRING, 
            matched_drugeffect, overwrite=overwrite)
    match_smoothed_drugeffect(therapy_test, smoothed_drugeffect_STRING,
            matchedtest_drugeffect, overwrite=overwrite)
    match_smoothed_drugeffect(therapy_leader, smoothed_drugeffect_STRING,
            matchedleader_drugeffect, overwrite=overwrite)


def test_match_doseresponsecoef(with_small, overwrite): 
    from pydream2015.feature.match import match_doseresponsecoef 
    match_doseresponsecoef(therapy, matched_doseresponsecoef, 
            overwrite=overwrite)
    match_doseresponsecoef(therapy_test, matchedtest_doseresponsecoef, 
            overwrite=overwrite)
    match_doseresponsecoef(therapy_leader, matchedleader_doseresponsecoef, 
            overwrite=overwrite)


