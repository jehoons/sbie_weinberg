# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import os, sys, cPickle as pickle, re, json, pandas as pd, numpy as np
from sets import Set
from multiprocessing import Pool
from os.path import exists, split as pathsplit, join
from pdb import set_trace
from ..util import update_progress

import pytest


def run_smoother(matfile, vecfile, res_smoothed, alpha=0.95, ncores=2,
        test=False): 
    """Mutation effect is simulated by using network smoothing algorithm(Hofree, 2013). The
    algorithm is based on randomwalk. This algorithm calculate the propagated effect of mutations.

    Args:
        inputs (a list of string): a list of input files
        - inputs[0]: mutated_gene_signals
        - inputs[1]: string_sco700_adj

        outputs (a list of string): a list of output files
        - outputs[0]: mut_smoothed
        - outputs[1]: mut_smoothed_corr

        args (a list of string): a list of arguments
        - args[0]: alpha value of the equation, F[i+1] = alpha*A*F[i] + (1-alpha)*F0

    Returns:
        N/A
    """

    if test: 
        ncores = 1

    adjmat = pd.read_csv(matfile, index_col='Unnamed: 0')
    signal = pd.read_csv(vecfile, index_col='Unnamed: 0')

    assert np.prod( adjmat.index == signal.index ) 

    # degree normalize: 
    for row in adjmat.index:
        if adjmat.loc[row].sum() > 0:
            adjmat.loc[row] = adjmat.loc[row] / adjmat.loc[row].sum()

    input_list = []
    for cell_line in signal.columns: 
        a_signal = signal[cell_line]
        input_list.append([cell_line, alpha, adjmat, a_signal, 1e-7, 500])

    if ncores > 1:
        p = Pool(ncores)
        smoothed_list = p.map(_randwalk_unit, input_list)
        p.close()
    else: 
        smoothed_list = [] 
        for n, inp in enumerate(input_list):
            update_progress(n, len(input_list))
            res = _randwalk_unit(inp,test)
            smoothed_list.append(res) 

    Fsmoothed_signal = signal.copy() 

    for smoothed in smoothed_list: 
        cell = smoothed['cell']
        fss = smoothed['FSS'] 
        Fsmoothed_signal[cell].loc[fss.index] = fss

    Fsmoothed_signal.to_csv(res_smoothed)


def _randwalk_unit(inp,test=False):
    cellline = inp[0]
    alpha = inp[1]
    A = inp[2]
    F0 = inp[3]
    eps = inp[4]
    steps = inp[5]
    return {'cell': cellline, 'FSS': _randwalk(alpha, A, F0, eps, steps,
        test)}


def _randwalk(alpha, A, F0, eps, steps, test=False):
    Fnext = np.zeros(F0.shape)
    Fprev = np.zeros(F0.shape)

    for i in range(1, steps):
        Fnext = alpha*A.dot(Fprev) + (1.0 - alpha)*F0
        error = np.sum( (Fprev - Fnext)**2 )

        if error < eps :
            break

        if test and (i > 10): 
            break 

        Fprev = Fnext
        
    return Fnext


def smooth_mutation_NCI(nci, sig, alp, mat, vec, smoothed, overwrite=False,
        test=False):
    if exists(smoothed) and (overwrite==False): 
        return 

    result_dir = pathsplit(smoothed)[0]

    smooth_mutation_NCI_pre(nci, sig, mat, vec, test=test) 

    print '[smoothing]'
    print '>>', smoothed
    run_smoother(mat, vec, smoothed, alpha=alp, ncores=4, test=test)


def smooth_mutation_NCI_pre(ppi, signal, filt_mat=None, filt_vec=None,
        test=False):

    mut = pd.read_csv(signal)

    cells = Set( mut['cell_line_name'].values.tolist() ) 
    cells = list(cells) 

    dream_nodes = Set( mut['Gene.name'].values.tolist() ) 

    n_dream = len(dream_nodes)

    nci_ppi = pd.read_csv(ppi, sep='\t', names=['item_id_a','item_id_b']) 

    _a = Set( nci_ppi['item_id_a'].values.tolist() )
    _b = Set( nci_ppi['item_id_b'].values.tolist() )

    NCI_nodes = _a.union( _b )
    n_nci = len(NCI_nodes) 

    common_nodes = NCI_nodes.intersection(dream_nodes)
    common_nodes = list(common_nodes)
    n_common = len(common_nodes) 

    adjmat_data = np.zeros([len(common_nodes), len(common_nodes)]) 
    adjmat = pd.DataFrame(adjmat_data, index=common_nodes, columns=common_nodes)

    for k, row in enumerate(nci_ppi.index):
        update_progress(k, nci_ppi.index.shape[0]) 

        node_a = nci_ppi.loc[row, 'item_id_a']
        node_b = nci_ppi.loc[row, 'item_id_b']

        if (node_a in adjmat.index) and (node_b in adjmat.index): 
            adjmat.loc[node_a, node_b] = 1

        if test and (k > 100): 
            break 

    if filt_mat != None: 
        adjmat.to_csv(filt_mat)

    signal_mat = np.zeros([adjmat.shape[0], len(cells)])
    vec = pd.DataFrame(signal_mat, index=adjmat.index, columns=cells)

    for k, row in enumerate(mut.index): 
        update_progress(k, mut.index.shape[0]) 
        cell_line_name = mut.loc[row, 'cell_line_name']
        gene_name = mut.loc[row, 'Gene.name'] 

        if (cell_line_name in vec.columns) and (gene_name in vec.index):
            vec.loc[gene_name, cell_line_name] = 1 

        if test and (k > 100): 
            break 

    if filt_vec != None: 
        vec.to_csv(filt_vec)

    print '#dream:%d, #NCI:%d, #common:%d' % (n_dream, n_nci, n_common)

    return adjmat, vec


def smooth_mutation_STRING_pre(ppi, signal, score_threshold=950, filt_mat=None,
        filt_vec=None, test=False):

    mut = pd.read_csv(signal)

    cells = Set( mut['cell_line_name'].values.tolist() ) 
    cells = list(cells) 

    dream_nodes = Set( mut['Gene.name'].values.tolist() ) 

    n_dream = len(dream_nodes)

    dfppi = pd.read_csv(ppi) 

    selected_ppi = dfppi.loc[dfppi['score'] > score_threshold]

    print 'theshold:%f, #original: %d, #filtered: %d'% (score_threshold, 
            dfppi.shape[0], selected_ppi.shape[0])

    _a = Set( selected_ppi['item_id_a'].values.tolist() )
    _b = Set( selected_ppi['item_id_b'].values.tolist() )

    ppi_nodes = _a.union( _b )
    num_ppi_nodes = len(ppi_nodes) 

    common_nodes = ppi_nodes.intersection(dream_nodes)
    common_nodes = list(common_nodes)
    n_common = len(common_nodes) 

    adjmat_data = np.zeros([len(common_nodes), len(common_nodes)]) 
    adjmat = pd.DataFrame(adjmat_data, index=common_nodes, columns=common_nodes)

    for k, row in enumerate(selected_ppi.index):
        update_progress(k, selected_ppi.index.shape[0]) 

        node_a = selected_ppi.loc[row, 'item_id_a']
        node_b = selected_ppi.loc[row, 'item_id_b']

        if (node_a in adjmat.index) and (node_b in adjmat.index): 
            adjmat.loc[node_a, node_b] = 1

        if test and (k>1000): 
            break 

    if filt_mat != None: 
        adjmat.to_csv(filt_mat)

    signal_mat = np.zeros([adjmat.shape[0], len(cells)])
    vec = pd.DataFrame(signal_mat, index=adjmat.index, columns=cells)

    for k, row in enumerate(mut.index): 
        update_progress(k, mut.index.shape[0]) 
        cell_line_name = mut.loc[row, 'cell_line_name']
        gene_name = mut.loc[row, 'Gene.name'] 

        if (cell_line_name in vec.columns) and (gene_name in vec.index):
            vec.loc[gene_name, cell_line_name] = 1 

        if test and (k>1000): 
            break 

    if filt_vec != None: 
        vec.to_csv(filt_vec)

    print '#dream:%d, #STRING:%d, #common:%d' % (n_dream, num_ppi_nodes, n_common)


def smooth_mutation_STRING(ppi, signal, mat, vec, smoothed, score, alp,
        overwrite=False, test=False):
    if exists(smoothed) and (overwrite==False): return 

    smooth_mutation_STRING_pre(ppi, signal, score_threshold=score, 
            filt_mat=mat, filt_vec=vec, test=test) 

    run_smoother(mat, vec, smoothed, alpha=alp, ncores=4,
            test=test)


def smooth_drugtarget(in_adjmat, in_druginfo, out_targetable, out_untargetable,
        out_druginfo_extended, out_smoothed, alpha=0.95, ncores=4, test=False,
        overwrite=False): 
    if exists(out_smoothed) and (overwrite==False): return 

    smooth_drugtarget_pre(in_adjmat, in_druginfo, out_targetable, out_untargetable, 
            out_druginfo_extended)
    
    df1 = pd.read_csv(in_adjmat, index_col='Unnamed: 0')
    df2 = pd.read_csv(out_targetable, index_col='Unnamed: 0')

    assert np.prod(df1.index == df2.index) == True

    run_smoother(in_adjmat, out_targetable, out_smoothed, alpha=alpha,
            ncores=ncores, test=test)


def smooth_drugtarget_pre(in_ppi, in_druginfo, out_targetable, out_untargetable, 
        out_druginfo2, overwrite=False):
    if exists(out_targetable) and (overwrite==False): return 

    sunghwan_list = {
            'BRAF_V600E': ['BRAF'], 
            'BRAF_mut': ['BRAF', 'CRAF'], 
            'CD19antibody': ['CD19'], 
            'CHK1': ['CHEK1'], 
            'NAE2': ['UBA3'], 
            'NIAP': ['BIRC1'], 
            'Proteasome': ['PSMC', 'PSMA'], 
            'TIE2': ['TEK'], 
            'TNFA': ['TNF'], 
            #'Thiamine': ['SLC19A2'], 
            'VEGFR2': ['KDR'], 
            'cMET': ['MET'], 
            #'Methylation': ['DNMT1','DNMT2','DNMT3'],
            #'Gammasecretase': ['APH1A'],
            'DNA': ['ATM','ATR'],
            }

    adjmat = pd.read_csv(in_ppi, index_col='Unnamed: 0') 
    ppi_node_list = adjmat.index.values.tolist()

    df_drug_info = pd.read_csv(in_druginfo)
    col_name = 'ChallengeName'
    col_target = 'Target(Official Symbol)'
    drugdata = {}

    for idx in df_drug_info.index:
        name = df_drug_info.loc[idx, col_name]
        target_string = df_drug_info.loc[idx, col_target]
        target_string = target_string.replace(' ', '')
        targets = target_string.split(',') 
        for n, target in enumerate(targets):
            if sunghwan_list.has_key(target):
                targets[n] = ",".join(sunghwan_list[target])

        _s = ",".join(targets)
        targets = _s.split(',')
        drugdata[name] = {'targets': targets}
    
    # here, we process the '*' character. 
    for drug in drugdata: 
        targets = drugdata[drug]['targets']
        drugdata[drug]['targetable'] = []
        drugdata[drug]['untargetable'] = []
        for n, target in enumerate(targets):
            if target.find('*') > 0: 
                # targets including '*', can be extended with the method of
                # regular expressions.
                rep = re.compile( target.replace('*', '.+') )
                matched = []
                for node in ppi_node_list:
                    res = rep.match(node)
                    if res is not None:
                        matched.append(res.group(0))

                if len(matched) == 0:
                    drugdata[drug]['untargetable'].append(target) 
                else:
                    drugdata[drug]['targetable'] += matched

            else: 
                # check if target is IN ppi_node_list
                if target in ppi_node_list:
                    drugdata[drug]['targetable'].append(target) 
                else: 
                    drugdata[drug]['untargetable'].append(target)

    for d in drugdata.keys():
        source_id = df_drug_info.loc[df_drug_info['ChallengeName'] == d, \
                'ChallengeName']

        smiles = df_drug_info.loc[df_drug_info['ChallengeName'] == d, \
                'SMILES or PubChem ID'].values[0]

        drugdata[d]['source_id'] = source_id 
        drugdata[d]['smiles'] = smiles
        drugdata[d]['all_targets'] = drugdata[d]['targetable'] + \
                drugdata[d]['untargetable']

    k = 1 
    for idx in df_drug_info.index:
        name = df_drug_info.loc[idx, col_name]
        alltargets = drugdata[name]['targetable'] + drugdata[name]['untargetable']
        # print 'all:', alltargets
        df_drug_info.loc[idx, 'sbie_id'] = ('sbiedrug%d_'%k) + name
        df_drug_info.loc[idx, 'drug_targets'] = ";".join(alltargets)
        k += 1

    df_drug_info.to_csv(out_druginfo2)

    untargetable_list = []
    targetable_list = []
    count_drugs_target = 0      # targetable을 포함하는 드럭의 갯수 
    count_drugs_untarget = 0 
    for drug in drugdata: 
        untargetable_list += drugdata[drug]['untargetable']  
        targetable_list += drugdata[drug]['targetable']

    colnames_untargetable = list(Set(untargetable_list))
    colnames_targetable = ppi_node_list

    df_untargetable = pd.DataFrame([], columns=colnames_untargetable)

    for drug in drugdata: 
        untargetable_list = drugdata[drug]['untargetable']
        df_untargetable.loc[drug] = np.zeros(len(colnames_untargetable))
        for untargetable in untargetable_list: 
            df_untargetable.loc[drug, untargetable] = 1 

    df_untargetable.fillna(0, inplace=True)  
    df_untargetable.T.to_csv(out_untargetable)

    df_targetable = pd.DataFrame([], columns=colnames_targetable)

    for drug in drugdata: 
        targetable_list = drugdata[drug]['targetable']
        df_targetable.loc[drug] = np.zeros(len(colnames_targetable))
        for targetable in targetable_list:
            df_targetable.loc[drug, targetable] = 1

    df_targetable.fillna(0, inplace=True) 
    df_targetable.T.to_csv(out_targetable)



