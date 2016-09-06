# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import os, sys, cPickle as pickle, re, json, pandas as pd, numpy as np, pytest
from sets import Set
from multiprocessing import Pool
from os.path import exists, split as pathsplit, join
from pdb import set_trace
from os.path import split,join

import pydream2015 

indir = join(split(pydream2015.__file__)[0], 'test_input')
outdir = join(split(pydream2015.__file__)[0], 'test_output')

pydream2015.initdatapath(indir, outdir)

from pydream2015.feature.smoother import smooth_drugtarget_pre
from pydream2015.feature.smoother import smooth_drugtarget
from pydream2015.feature.smoother import run_smoother


def test_smooth_mutation_STRING(with_small, overwrite):

    score = 950 
    alp = 0.95

    ppi = pydream2015.MYDATA_PPI_STRING_TRANSLATED
    signal = pydream2015.DATA_MUTATION
    mat = pydream2015.MYDATA_MUTSMOOTH_MAT_STRING 
    vec = pydream2015.MYDATA_MUTSMOOTH_VEC_STRING
    resfile = pydream2015.MYDATA_SMOOTHED_MUTATION_STRING

    pydream2015.feature.smoother.smooth_mutation_STRING(ppi,signal,mat,vec, 
            resfile,score,alp,overwrite=overwrite) 


def test_smooth_mutation_NCI(with_small, overwrite): 

    alp = 0.95 

    in_ppi = pydream2015.DATA_PPI_NCI
    in_signal = pydream2015.DATA_MUTATION

    out_mat = pydream2015.MYDATA_MUTSMOOTH_MAT_NCI
    out_vec = pydream2015.MYDATA_MUTSMOOTH_VEC_NCI

    out_smoothed = pydream2015.MYDATA_SMOOTHED_MUTATION_NCI
    
    pydream2015.feature.smoother.smooth_mutation_NCI(in_ppi, in_signal, alp, 
            out_mat, out_vec, out_smoothed, overwrite=overwrite)


@pytest.mark.skipif('True')
def test_run_smoother(): 

    matfile = '../test_input/devel/run_smoother/matrix.csv'
    vecfile = '../test_input/devel/run_smoother/vectors.csv'

    outfile = '__tmp_run_smoother.csv'

    run_smoother(matfile, vecfile, outfile) 


def test_smooth_drugtarget(with_small, overwrite): 

    ppi = 'STRING' # or 'NCI'

    if ppi == 'STRING': 
        in_adjmat = pydream2015.MYDATA_MUTSMOOTH_MAT_STRING
        out_smoothed = pydream2015.MYDATA_SMOOTHED_DRUGEFFECT_STRING

    elif ppi == 'NCI':
        in_adjmat = pydream2015.MYDATA_MUTSMOOTH_MAT_NCI
        out_smoothed = pydream2015.MYDATA_SMOOTHED_DRUGEFFECT_NCI

    else:
        assert False 

    in_druginfo = pydream2015.DATA_DRUG_INFO 
    out_druginfo_extended = pydream2015.MYDATA_DRUG_INFO_EXT
    out_targetable = pydream2015.MYDATA_DRUG_TARGET_ABLE
    out_untargetable = pydream2015.MYDATA_DRUG_TARGET_UNABLE

    smooth_drugtarget(in_adjmat, in_druginfo, out_targetable, out_untargetable, 
            out_druginfo_extended, out_smoothed, alpha=0.95, ncores=4,
            overwrite=overwrite)

    assert exists(out_druginfo_extended) 
    assert exists(out_targetable) 
    assert exists(out_untargetable) 
    assert exists(out_smoothed)


