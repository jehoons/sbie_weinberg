# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************

import pandas as pd 
import pdb 
import json
import itertools 
from os.path import join,dirname

treatment_file = join(dirname(__file__), 'Demo_drug_response.csv')
output_dir = dirname(__file__)

import pytest 
import glob
import json 

from pdb import set_trace

from sbie_weinberg.module import dream2015


def make_range_demo(outfile='range.json'):

    df = pd.read_csv(treatment_file)

    celltypes = set(df['Primary Cell Line Name'])
    celltypes = [el.replace(' ', '') for el in celltypes]

    drugs = set(df['Compound'])
    drugs = [el for el in drugs]

    input_range = {'range': { 'cell': celltypes, 'drug': drugs }}

    with open(outfile, 'w') as outfobj: 
        json.dump(input_range, outfobj, indent=4, sort_keys=True, \
            separators=(',',':'))


def make_range_dream2015(outfile='range_dream2015.json'): 

    datadir = join(dirname(dream2015.__file__), 
        'code-with-inputdata')

    """ this module calculates the range of cells and drugs from dataset """
    df1 = pd.read_csv(datadir+'/THERAPY_TRAINSET.CSV') 
    df2 = pd.read_csv(datadir+'/THERAPY_TESTSET.CSV')

    cells = set( df1['CELL_LINE'].tolist() + df2['CELL_LINE'].tolist() )
    drugs = set( df1['COMPOUND_A'].tolist() + df2['COMPOUND_B'].tolist() )

    simul_range = { 
        'range': {
            'cell': [el for el in cells], 
            'drug': [el for el in drugs], 
            }
        }

    with open('range_dream2015.json', 'w') as foutjson:
        json.dump(simul_range, foutjson, indent=4, sort_keys=True, separators=(',', ':'))    


def make_inputdata_combination(infile='range_dream2015.json', combi_numbers=[2], \
        outputheader='demoinput_dream2015_', limit=10):

    # combi_numbers = [ 2 ]
    # outputheader = 'demoinput_dream2015_'
    
    with open(infile, 'r') as finp: 
        datadict = json.load(finp)

    drugs = datadict['range']['drug']
    cells = datadict['range']['cell']

    drugs_list = [] 

    for i in combi_numbers:
        for d in itertools.combinations(drugs, i):
            drugs_list.append(d)

    inputjson_list = [] 
    for thiscell in cells: 
        for drugmembers in drugs_list: 
            inputjson = {
                'input': {
                    'celltype': thiscell, 
                    'drugs': [el for el in drugmembers]
                    }
                }
            inputjson_list.append(inputjson)

    for i,inputjson in enumerate(inputjson_list):
        outputfilename = join(output_dir, outputheader+'%d.json' % i)        
        with open(outputfilename, 'w') as outfile: 
            json.dump(inputjson, outfile, indent=4, sort_keys=True,
                separators=(',',':'))

        if i > limit: 
            break                 



