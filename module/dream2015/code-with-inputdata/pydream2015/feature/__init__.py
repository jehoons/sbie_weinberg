# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
__all__ = ['smoother', 'calc_dd3d', 'prepare', 'test_match_user']

import os,sys
import pandas as pd, numpy as np 
from os.path import join,exists,split as pathsplit
from os import remove 

# import cPickle as pickle 
import pickle
import pytest

from ..util import update_progress

from pdb import set_trace

def calc_dd3d(drug_3d, drug_3d_conv):

    dfdesc3d = pd.read_csv(drug_3d, index_col='Name')
    conv_lbls = range(0, dfdesc3d.columns.shape[0]*2-1)
    fout = open(drug_3d_conv, 'wb')
    header = ['drug_a', 'drug_b'] + ['%d'%v for v in conv_lbls] 
    strdata = [ ",".join(header) ] 
    k = 0 
    for i in dfdesc3d.index: 
        for j in dfdesc3d.index: 
            update_progress(k, len(dfdesc3d.index)**2) 
            idata = dfdesc3d.loc[i]
            jdata = dfdesc3d.loc[j] 
            value = np.convolve(idata, jdata)
            words = [i, j] + ['%e'%v for v in value.tolist()]
            strdata.append( ",".join( words ) ) 
            k += 1

    fout.write( "\n".join(strdata ) )
    fout.close()


#def test_calc_dd3d():
#    sys.path.append('../..')
#    import pydream2015
#    pydream2015.initdatapath('../test_input', '../test_output')
#
#    in_dd3d = pydream2015.DATA_DRUG_DESC_3D
#    out_dd3d_conv = pydream2015.MYDATA_DRUG_DESC_3D_CONV
#
#    if not exists(out_dd3d_conv):
#        calc_dd3d(in_dd3d, out_dd3d_conv) 
#    else: 
#        print '>>', out_dd3d_conv, '- skipped'
#

def collect_feature(matched_list, with_small=False, mode='train'):

    def small(name):
        return join(pathsplit(name)[0], 'small_' + pathsplit(name)[1]) 

    X = None

    for i, matched in enumerate(matched_list):

        if mode == 'train': 
            pass 

        elif mode == 'test': 
            matched = matched.replace('matched','matchedtest')
            pass

        elif mode == 'leader':
            matched = matched.replace('matched','matchedleader')
            pass

        elif mode == 'user':
            matched = matched.replace('matched','matcheduser')
            pass

        else: 
            """ mode = train, test, leader, or user """ 
            assert False 

        if with_small: 
            matched = small(matched) 

        if i == 0: 
            X = pickle.load(open(matched, 'rb'))

        else: 
            X1 = pickle.load(open(matched, 'rb'))  
            X = pd.merge(X, X1, left_index=True, right_index=True, how='left')

    return X 


