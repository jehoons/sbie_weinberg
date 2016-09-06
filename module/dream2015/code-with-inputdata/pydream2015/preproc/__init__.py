# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
__all__ = ['fill_missinggex','make_biomartsdict','translate_STRING']

import os,sys
import pandas as pd, numpy as np 
from sets import Set
from os.path import join 
from os.path import exists 
from os import remove 

from ..util import update_progress

# import cPickle as pickle 
import pickle
import pytest


def fill_missinggex(therapy, gexfile, cellinfofile, filled_gex):
    # input:
    #   therapy, gexfile, cellinfofile
    # output: 
    #   filled_gex 
    print ('[fill_missinggex]')
    print ('<<', therapy)
    print ('<<', gexfile)
    print ('<<', cellinfofile)
    print ('>>', filled_gex )

    therapy = pd.read_csv(therapy)
    gex = pd.read_csv(gexfile, index_col='Unnamed: 0')
    gex = gex.T

    cells_in_therapy = Set( therapy['CELL_LINE'].values.tolist() )
    cells_in_gex = Set( gex.index.values.tolist() )
    missing_cells = cells_in_therapy - cells_in_gex

    # fill the missing cells with the cells originated from same tissue
    # so, first we need the families that shares the same tissue location.
    cellinfo = pd.read_csv(cellinfofile)
    miss_cell_info = {}

    for cell in missing_cells: 
        tissue = cellinfo.loc[ cellinfo['Sanger.Name'] == cell,\
                'Tissue..General.' ]
        cellfamily = cellinfo.loc[ cellinfo['Tissue..General.'] ==\
                tissue.values.tolist()[0], 'Sanger.Name']

        miss_cell_info[ cell ] = {} 
        miss_cell_info[ cell ][ 'tissue' ] = tissue.values.tolist()[0]
        miss_cell_info[ cell ][ 'family' ] = cellfamily.values.tolist()

    for cell in miss_cell_info.keys():
        cellinfo = miss_cell_info[cell]
        family = gex.loc[cellinfo['family']]
        gex.loc[cell] = family.mean()

    gex.T.to_csv(filled_gex)


def make_biomartsdict(biomarts_csv, biomart_dict, test=False):
    print ('[make_biomartsdict]')
    print ('<<', biomarts_csv) 
    print ('>>', biomart_dict)

    ensembletbl = pd.read_csv(biomarts_csv)
    ensp_node_set  = Set(ensembletbl['Ensembl Protein ID'].values)
    ensp_node_set -= Set([np.nan])
    ensp_id_list = list(ensp_node_set)
    ensp_to_gene = {} 

    for i, ensp_id in enumerate(ensp_id_list):
        hgnc_symbol = ensembletbl.loc[ ensembletbl['Ensembl Protein ID'] ==
                ensp_id, 'HGNC symbol']
        hgnc_symbol_value = hgnc_symbol.values
        ensp_to_gene[ensp_id] = hgnc_symbol_value

        update_progress(i, len(ensp_id_list))

        if (i > 100) and test: 
            update_progress(len(ensp_id_list), len(ensp_id_list))
            break 
    
    savedir = os.path.split(biomart_dict)[0]

    if not exists(savedir):
        os.makedirs(savedir)

    fobj = open(biomart_dict, 'wb')
    pickle.dump(ensp_to_gene, fobj)
    fobj.close()


def translate_STRING(ppifile, enspdic, processedppi, translatedppi, ppihist,
        test=False):

    # input - ppifile, enspdic
    # output - processedppi, translatedppi, ppihist 
    print '[translate_STRING]'
    print '<<', ppifile
    print '<<', enspdic
    print '>>', processedppi
    print '>>', translatedppi
    print '>>', ppihist

    fobj = open(processedppi, 'wb')
    fobj.write('protein1,protein2,combined_score\n')
    num_lines = sum(1 for line in open(ppifile))
    for i,l in enumerate(file(ppifile)):
        update_progress(i, num_lines)  
        l = l.strip()
        words = l.split()
        source = words[0].split('.')[1]
        target = words[1].split('.')[1]
        score = float(words[2])
        fobj.write('%s,%s,%f\n' % (source, target, score))
        if test and (i > 50):
            break 

    fobj.close()

    ppi = pd.read_csv(processedppi)
    counts, bins = np.histogram(ppi['combined_score'])
    ppi_hist = pd.DataFrame(pd.Series(counts, index=bins[:-1]), \
            columns=['frequency'])
    ppi_hist['frequency(%)'] = \
            ppi_hist['frequency'] / ppi_hist['frequency'].sum()*100.0

    ppi_hist.to_csv(ppihist)

    ensp_to_gene = pickle.load(open(enspdic, 'rb'))

    fobj = open(translatedppi,'wb')
    num_lines = sum(1 for line in open(processedppi))
    for i,l in enumerate(file(processedppi)):
        l = l.strip()
        if i == 0: 
            continue 
        update_progress(i, num_lines) 
        words = l.split(',')
        prot1 = words[0]
        prot2 = words[1]
        score = words[2]

        if ensp_to_gene.has_key(prot1) and ensp_to_gene.has_key(prot2):
            g1 = ensp_to_gene[prot1]
            g2 = ensp_to_gene[prot2]
            if g1[0] != 'nan' and g2[0] != 'nan':
                fobj.write('%s,%s,%s\n' % (g1[0], g2[0], score))

    fobj.close()

    ppi_df = pd.read_csv(translatedppi, \
            names=['item_id_a', 'item_id_b', 'score'])
    ppi_df.drop( ppi_df.index[ ppi_df.isnull().any(axis=1) ], inplace=True)
    ppi_df.to_csv(translatedppi, index=False )


def test_make_biomartsdict(): 

    sys.path.append('../..')
    import pydream2015

    pydream2015.initdatapath('../test_input', '../test_output')

    in_ensemblid = pydream2015.DATA_ENSEMBLID 
    out_dict = pydream2015.MYDATA_DICT

    print '>>', out_dict

    if not exists(out_dict):
        make_biomartsdict(in_ensemblid, out_dict, test=False)
    else:
        print '- skipped'

    assert exists(out_dict)


def test_fill_missinggex():

    sys.path.append('../..')
    import pydream2015

    pydream2015.initdatapath('../test_input', '../test_output')

    in_therapy = pydream2015.DATA_COMBITHERAPY
    in_gex = pydream2015.DATA_GENEEXPR 
    in_cellinfo = pydream2015.DATA_CELLINFO 
    out_gexfilled = pydream2015.MYDATA_GENEEXPR_FILLED 

    fill_missinggex(in_therapy, in_gex, in_cellinfo, out_gexfilled)

    assert exists(out_gexfilled)

# @pytest.mark.skipif('True')
def test_translate_STRING():

    sys.path.append('../..')
    import pydream2015

    pydream2015.initdatapath('../test_input', '../test_output')

    in_ppi = pydream2015.DATA_PPI_STRING 
    in_dict = pydream2015.MYDATA_DICT
    out_processed = pydream2015.MYDATA_PPI_STRING_PROCESSED
    out_translated = pydream2015.MYDATA_PPI_STRING_TRANSLATED 
    out_hist = pydream2015.MYDATA_PPI_STRING_HIST

    translate_STRING(in_ppi, in_dict, out_processed, out_translated, out_hist, 
            test=False)

    assert exists(out_processed)
    assert exists(out_translated) 
    assert exists(out_hist) 


