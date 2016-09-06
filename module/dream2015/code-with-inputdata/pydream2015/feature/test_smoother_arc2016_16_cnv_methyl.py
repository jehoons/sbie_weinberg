# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
# 이 모듈은 민수가 전처리한 CNV, Methyl 프로화일을 이용하여 smoothing 파일을 
# 생성한다.
import os,sys,re,time,datetime,itertools,getopt,json,glob,pytest
import pandas as pd, numpy as np, cPickle as pickle
from sets import Set

from pdb import set_trace
from os.path import exists
from os.path import split as pathsplit
from os.path import join

from pydream2015.util import update_progress
from pydream2015.feature import smoother


def preproc(gexfile, ppi, signal, score_threshold=950, filt_mat=None, 
        filt_vec=None):

    gexprofile_df = pd.read_csv(gexfile,index_col='Unnamed: 0')
    gex_cells = gexprofile_df.columns.values.tolist() 

    # df_signal 은 다음과 같이 가정된다: 
    # genes x cells

    df_signal = pd.read_csv(signal, index_col='Unnamed: 0')
    df_signal[df_signal == 'Selected'] = 1.0  

    sig_cells = Set( df_signal.columns.values.tolist() ) 
    sig_cells = list(sig_cells) 

    sig_nodes = Set( df_signal.index.values.tolist() ) 

    n_dream = len(sig_nodes)

    dfppi = pd.read_csv(ppi) 

    selected_ppi = dfppi.loc[dfppi['score'] > score_threshold]

    print 'theshold:%f, #original: %d, #filtered: %d'% (score_threshold, 
            dfppi.shape[0], selected_ppi.shape[0])

    _a = Set( selected_ppi['item_id_a'].values.tolist() )
    _b = Set( selected_ppi['item_id_b'].values.tolist() )

    ppi_nodes = _a.union( _b )
    num_ppi_nodes = len(ppi_nodes) 

    common_nodes = ppi_nodes.intersection(sig_nodes)
    common_nodes = list(common_nodes)
    n_common = len(common_nodes) 

    adjmat_data = np.zeros([len(common_nodes), len(common_nodes)]) 
    adjmat = pd.DataFrame(adjmat_data, index=common_nodes, columns=common_nodes)

    # matrix 파일의 생성
    for k, row in enumerate(selected_ppi.index):
        update_progress(k, selected_ppi.index.shape[0]) 

        node_a = selected_ppi.loc[row, 'item_id_a']
        node_b = selected_ppi.loc[row, 'item_id_b']

        if (node_a in adjmat.index) and (node_b in adjmat.index): 
            adjmat.loc[node_a, node_b] = 1

    if filt_mat != None: 
        print '>>', filt_mat
        adjmat.to_csv(filt_mat)

    # vector 파일의 생성 
    # test
    # gex_cells += ['cell0']
    signal_mat = np.zeros([adjmat.shape[0], len(gex_cells)])
    # vec = pd.DataFrame(signal_mat, index=adjmat.index, columns=sig_cells)
    
    vec = pd.DataFrame(signal_mat, index=adjmat.index, columns=gex_cells)
    # vec은 gex_cells를 컬럼으로 가지고 있다. 이것은 셀라인의 기준이 되는 집합이
    # gex.csv파일에 들어있다고 가정하는 것이다. 만약 gex_cells가 sig_cells를
    # 모두 포함하지 않는다면, 문제가 vec에는 NA 값들이 존재하게 될것이다. 이것을
    # 막아야 한다.
    vec.loc[adjmat.index, sig_cells] = df_signal.loc[adjmat.index, sig_cells]

    assert vec.isnull().any().any() == False

    print '>>', filt_vec
    vec.to_csv(filt_vec) 

    print '#signal nodes:%d, #ppi nodes:%d, #common:%d' % (n_dream, 
            num_ppi_nodes, n_common)

    return adjmat, vec


def run(gexfile,ppifile,signalfile,resultfileptn,ppiscore,alpha,overwrite=False):
    resfile = resultfileptn
    if not exists(resfile) and (overwrite==False):
        # Step 1. 
        # 우선 매트릭스와 벡터파일을 생성한다. 이 파일들은 resultfileptn(smoothed)를
        # 만들기 위한 중간 결과이다. 
        # 중간파일들: 
        # outfileptn_mat, outfileptn_vec
        result_dir = pathsplit(resultfileptn)[0]
        outfileptn_mat = '_tmp_mat.csv' 
        outfileptn_vec = '_tmp_vec.csv' 
        filt_mat = join(result_dir, outfileptn_mat)
        filt_vec = join(result_dir, outfileptn_vec)
        print '[preprocessing]'
        preproc(gexfile, ppifile, signalfile, score_threshold=ppiscore, 
                filt_mat=filt_mat, filt_vec=filt_vec) 
        # Step 2. 
        # 매트릭스와 벡터파일을 생성한 후에는, 이들을 이용하여 스무딩을 수행한다.
        # 스무딩에는 alpha파라미터가 필요하다.
        print '- run randomwalk algorithm ...'
        smoother.run_smoother(filt_mat, filt_vec, resfile, alpha=alpha, 
                ncores=4)
    else: 
        print '- file already exists:', resfile


def test_ARC2016_16(with_small, overwrite):

    import pydream2015
    from os.path import split,join

    pkgdir = split(pydream2015.__file__)[0]

    input_dir = join(pkgdir, 'test_input') 
    output_dir = join(pkgdir, 'test_output') 

    pydream2015.initdatapath(input_dir, output_dir)

    ppiscore = 950 
    alpha = 0.95

    ppifile = pydream2015.MYDATA_PPI_STRING_TRANSLATED 
    gexfile = pydream2015.MYDATA_GENEEXPR_FILLED

    signalfile = join(input_dir, 'team/mschoi/arc2016_16_table(a)cnv.csv')
    resfile = 'smooth_cnv_str.csv'

    run(gexfile, ppifile, signalfile, resfile, ppiscore, alpha)

    signalfile = join(input_dir, 'team/mschoi/arc2016_16_table(b)methyl.csv')
    resfile = 'smooth_methyl_str.csv'

    run(gexfile, ppifile, signalfile, resfile, ppiscore, alpha)


