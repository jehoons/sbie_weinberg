# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
__all__ = ['open_rserv', 'close_rserv', 'cv_glmnet','ch1scoring_cv']

import os, time, numpy as np, tempfile, pyRserve
from numpy.random import randn
from os.path import exists 
from pdb import set_trace

conn = None

def open_rserv():
    global conn 
    conn = pyRserve.connect()


def close_rserv():
    global conn 
    conn.close()


def cv_glmnet(X, y, standardize=False, alpha=1.0, nfolds=5, ncores=1):

    global conn

    if conn == None:
        assert False 

    temp_x = tempfile.mktemp(suffix='.npy')
    temp_y = tempfile.mktemp(suffix='.npy')

    temp_yhat = tempfile.mktemp(suffix='.npy')
    temp_coeff = tempfile.mktemp(suffix='.npy')

    np.save(temp_x, X)
    np.save(temp_y, y.flatten())

    # input data
    conn.r.xfile = temp_x
    conn.r.yfile = temp_y

    # output data
    conn.r.yhatfile = temp_yhat
    conn.r.coeffile = temp_coeff

    # lasso parameters
    conn.r.standardize = standardize
    conn.r.alpha = alpha 
    conn.r.nfolds = nfolds 
    conn.r.ncores = ncores

    if ncores > 1:
        conn.r.parallel = True
    else:
        conn.r.parallel = False

    r_cmd = """
        require(RcppCNPy)
        require(glmnet) 
        require(doMC)
        registerDoMC(cores=50) 
        x <- npyLoad(xfile)
        y <- npyLoad(yfile)
        cvfit = cv.glmnet(x,y,standardize=standardize,alpha=alpha,nfolds=nfolds,
            parallel=TRUE)
        coefvalues = coef(cvfit, s=\'lambda.min\')
        coefvaluesMat = as.matrix(coefvalues)
        npySave(coeffile, coefvaluesMat)
        yhat <- predict(cvfit, newx=x, s="lambda.min")
        npySave(yhatfile, yhat)
        pearsonr <- cor(yhat, y)[1]
    """ 
    conn.voidEval(r_cmd)

    coef = np.load(temp_coeff) 
    yhat = np.load(temp_yhat) 
    pearsonr = conn.r.pearsonr

    return coef, yhat, pearsonr 

    
