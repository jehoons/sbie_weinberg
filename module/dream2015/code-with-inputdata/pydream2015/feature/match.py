# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import os, sys, re, json, pandas as pd, numpy as np, pytest
import pickle
# from sets import Set
from multiprocessing import Pool
from os.path import exists, split as pathsplit, join
from pdb import set_trace
from ..util import update_progress

__small = 10


def small(name):
    return join(pathsplit(name)[0], 'small_'+pathsplit(name)[1])
    

def match_gex(therapy, gex, outfile, overwrite=False):
    if exists(outfile) and (overwrite==False):
        return 

    therapy_df = pd.read_csv(therapy) 
    gex_df = pd.read_csv(gex, index_col='Unnamed: 0') 
    gex_df = gex_df.T 

    therapy_cells = set( therapy_df['CELL_LINE'].values.tolist() )
    gex_cells = set( gex_df.index.values.tolist() ) 
    assert therapy_cells.issubset(gex_cells)

    therapy_df = pd.merge(therapy_df[['CELL_LINE']], gex_df, left_on='CELL_LINE',
            right_index=True, how='left')
    assert therapy_df.isnull().any().any() == False

    matched_gex_df = therapy_df[gex_df.columns].copy(deep=True) 
    matched_gex_df.rename(columns=__attach(matched_gex_df.columns,
        'GEX.'), inplace=True)

    pickle.dump(matched_gex_df, open(outfile,'wb'))
    pickle.dump(matched_gex_df[matched_gex_df.columns[0:__small]], 
            open(small(outfile),'wb'))

    return 


def match_mut(therapy, mutation, outfile, overwrite=False):
    if exists(outfile) and (overwrite==False): 
        return 

    therapy_df = pd.read_csv(therapy) 
    mut_df = pd.read_csv(mutation) 
    
    mut_genes = set( mut_df['Gene.name'].values.tolist() )
    mut_cells = set( mut_df['cell_line_name'].values.tolist() )

    therapy_cells = set( therapy_df['CELL_LINE'].values.tolist() )
    assert therapy_cells.issubset(mut_cells)

    mut_dense = pd.DataFrame([], index=list(mut_cells),
            columns=list(mut_genes))

    for i, row in enumerate(mut_df.index): 
        update_progress(i, mut_df.shape[0])
        gene = mut_df.loc[row, 'Gene.name']
        cell = mut_df.loc[row, 'cell_line_name']
        mut_dense.loc[cell, gene] = 1 
   
    mut_dense.fillna(0, inplace=True) 

    therapy_df = pd.merge(therapy_df[['CELL_LINE']], mut_dense, 
            left_on='CELL_LINE', right_index=True, how='left')

    assert therapy_df.isnull().any().any() == False

    matched_mut_df = therapy_df[list(mut_genes)].copy(deep=True) 
    matched_mut_df.rename(columns=__attach(matched_mut_df.columns,
        'MUT.'), inplace=True)

    pickle.dump(matched_mut_df, open(outfile,'wb'))
    pickle.dump(matched_mut_df[matched_mut_df.columns[0:__small]], 
            open(small(outfile),'wb'))

    return 


def match_smoothed_CNV(therapy, cnv, outfile, overwrite=False):
    if exists(outfile) and (overwrite==False): 
        return 

    therapy_df = pd.read_csv(therapy) 
    cnv_df = pd.read_csv(cnv, index_col='Unnamed: 0') 
    cnv_df = cnv_df.T 

    therapy_cells = set( therapy_df['CELL_LINE'].values.tolist() )
    cnv_cells = set( cnv_df.index.values.tolist() ) 
    assert therapy_cells.issubset(cnv_cells)

    therapy_df = pd.merge(therapy_df[['CELL_LINE']], cnv_df, left_on='CELL_LINE',
            right_index=True, how='left')
    assert therapy_df.isnull().any().any() == False

    matched_cnv_df = therapy_df[cnv_df.columns].copy(deep=True) 
    matched_cnv_df.rename(columns=__attach(matched_cnv_df.columns,
        'CNV.'), inplace=True)

    pickle.dump(matched_cnv_df, open(outfile,'wb'))
    pickle.dump(matched_cnv_df[matched_cnv_df.columns[0:__small]], 
            open(small(outfile),'wb'))

    return 


def match_smoothed_methyl(therapy, methyl, outfile, overwrite=False):
    if exists(outfile) and (overwrite==False):
        return 

    therapy_df = pd.read_csv(therapy) 
    methyl_df = pd.read_csv(methyl, index_col='Unnamed: 0') 
    methyl_df = methyl_df.T 

    therapy_cells = set( therapy_df['CELL_LINE'].values.tolist() )
    methyl_cells = set( methyl_df.index.values.tolist() ) 

    assert therapy_cells.issubset(methyl_cells)

    therapy_df = pd.merge(therapy_df[['CELL_LINE']], methyl_df, left_on='CELL_LINE',
            right_index=True, how='left')
    assert therapy_df.isnull().any().any() == False

    matched_methyl_df = therapy_df[methyl_df.columns].copy(deep=True)
    matched_methyl_df.rename(columns=__attach(matched_methyl_df.columns,
        'METH.'), inplace=True)

    pickle.dump(matched_methyl_df, open(outfile,'wb'))
    pickle.dump(matched_methyl_df[matched_methyl_df.columns[0:__small]], 
            open(small(outfile),'wb'))

    return 


def match_dd3dc(therapy, dd3dc, outfile, overwrite=False):
    if exists(outfile) and (overwrite==False):
        return 

    therapy_df = pd.read_csv(therapy) 
    dd3dc_df = pd.read_csv(dd3dc)
    
    for i in dd3dc_df.index:
        drug_a = dd3dc_df.loc[i, 'drug_a']
        drug_b = dd3dc_df.loc[i, 'drug_b']
        combi_drug = drug_a + '.' + drug_b
        dd3dc_df.loc[i, 'COMBINATION_ID'] = combi_drug

    therapy_df = pd.merge(therapy_df[['COMBINATION_ID']], dd3dc_df, 
            left_on='COMBINATION_ID', right_on='COMBINATION_ID', how='left')

    assert therapy_df.isnull().any().any() == False

    matched_dd3dc_df = therapy_df[dd3dc_df.columns[2:-1]].copy(deep=True)
    matched_dd3dc_df.rename(columns=__attach(matched_dd3dc_df.columns,
        'DD3DC.'), inplace=True)

    pickle.dump(matched_dd3dc_df, open(outfile,'wb'))
    pickle.dump(matched_dd3dc_df[matched_dd3dc_df.columns[0:__small]], 
            open(small(outfile),'wb'))

    return 


def __attach(old_columns, col_header):
    new_cols = {} 
    for col in old_columns:
        new_cols[col] = col_header + col

    return new_cols 


def match_smoothed_mut_STRING(therapy, smoothed, outfile,
        overwrite=False):
    if exists(outfile) and (overwrite==False):
        return 

    therapy_df = pd.read_csv(therapy) 
    smoothed_df = pd.read_csv(smoothed, index_col='Unnamed: 0') 
    smoothed_df = smoothed_df.T 
    
    cols = smoothed_df.columns 

    therapy_df = pd.merge(therapy_df[['CELL_LINE']], smoothed_df, 
            left_on='CELL_LINE', right_index=True, how='left')

    assert therapy_df.isnull().any().any() == False

    matched_smoothed_df = therapy_df[cols].copy(deep=True)
    matched_smoothed_df.rename(columns=__attach(matched_smoothed_df.columns,
        'SMOOTH_MUT.'), inplace=True)
    pickle.dump(matched_smoothed_df, open(outfile,'wb'))
    pickle.dump(matched_smoothed_df[matched_smoothed_df.columns[0:__small]], 
            open(small(outfile),'wb'))

    return 


def match_smoothed_drugeffect(therapy, smoothed, outfile,
        overwrite=False):
    if exists(outfile) and (overwrite==False):
        return 

    therapy_df = pd.read_csv(therapy) 
    smoothed_df = pd.read_csv(smoothed, index_col='Unnamed: 0') 
    smoothed_df = smoothed_df.T 

    drug_a_effect = pd.merge(therapy_df[['COMPOUND_A']], smoothed_df, 
            left_on='COMPOUND_A', right_index=True, how='left')
    drug_b_effect = pd.merge(therapy_df[['COMPOUND_B']], smoothed_df, 
            left_on='COMPOUND_B', right_index=True, how='left')

    assert np.prod(drug_b_effect.columns[1:] == drug_a_effect.columns[1:]) == 1

    cols = drug_a_effect.columns[1:] 
    combidrugs_effect = drug_a_effect[cols] + drug_b_effect[cols]

    assert combidrugs_effect.isnull().any().any() == False

    combidrugs_effect.rename(columns=__attach(combidrugs_effect.columns, 
        'SMOOTH_DE.'), inplace=True)

    pickle.dump(combidrugs_effect, open(outfile,'wb'))
    pickle.dump(combidrugs_effect[combidrugs_effect.columns[0:__small]], 
            open(small(outfile),'wb'))

    return


def match_doseresponsecoef(therapy, outfile, overwrite=False):
    if exists(outfile) and (overwrite==False):
        return 

    therapy_df = pd.read_csv(therapy) 
    
    drc_cols = ['MAX_CONC_A', 'MAX_CONC_B', 'IC50_A', 'H_A', 'Einf_A', 'IC50_B', 
            'H_B', 'Einf_B']

    drc_df = therapy_df[drc_cols] 

    conv_lbls = range(0, drc_df.columns.shape[0]*2-1)

    for k, i in enumerate(drc_df.index):
        update_progress(k, len(drc_df.index))
        adata = drc_df.loc[i, ['MAX_CONC_A', 'IC50_A', 'H_A', 'Einf_A']]
        bdata = drc_df.loc[i, ['MAX_CONC_B', 'IC50_B', 'H_B', 'Einf_B']]
        value = np.convolve(adata,bdata)

        if i == 0: 
            dfconvres = pd.DataFrame([], columns=[ 'v%d' % _i for _i in 
                range(0, len(value))])
            pass

        dfconvres.loc[i] = value
        
    assert dfconvres.isnull().any().any() == False

    dfconvres.rename(columns=__attach(dfconvres.columns, 'DRCC.'), 
            inplace=True)

    dfconvres.sort(inplace=True) 

    assert set(therapy_df.index) == set(dfconvres.index)

    pickle.dump(dfconvres, open(outfile, 'wb'))
    pickle.dump(dfconvres[dfconvres.columns[0:__small]], 
            open(small(outfile),'wb'))

    return

