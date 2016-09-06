# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import os, time, numpy as np, sys
from pdb import set_trace
from os.path import exists,join,split
from pdb import set_trace

#def test_cv_glmnet(with_small, overwrite):
#   
#    import pydream2015
#    from pydream2015 import rlang
#
#    rlang.open_rserv() 
#
#    nsamps = 100
#    X = np.random.randn(nsamps, 4)
#    y = X[:,0:3].dot( np.array([[3.2],[4],[5]])) + 10 + np.random.randn(nsamps, 1)*2 
#
#    tic = time.time()
#    coeff, yhat, pearsonr = rlang.cv_glmnet(X, y, standardize=True, alpha=1.0, nfolds=5,
#            ncores=10) 
#
#    print coeff
#    print 'elapsed time: ', time.time() - tic
#
#    set_trace()
#
#    rlang.close_rserv()


def test_ch1scoring_fc(): 
    
    import pydream2015
    from pydream2015.rlang import ch1scoring_fc
    
    obs = join(split(ch1scoring_fc.__file__)[0], 'testdata_ch1scoring_fc_obs.csv')
    pred = join(split(ch1scoring_fc.__file__)[0], 'testdata_ch1scoring_fc_pred.csv')

    ch1scoring_fc.run(obs, pred)


