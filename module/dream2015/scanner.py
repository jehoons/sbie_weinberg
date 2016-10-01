from os.path import join,exists,dirname
from sbie_weinberg.module import dream2015
from sbie_weinberg.util import progressbar
import pandas as pd
from itertools import combinations
from sbie_weinberg.module.dream2015 import predictor 
from ipdb import set_trace
import json 

def get_range():

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

    return simul_range


def get_inputcombination():

    datadir = join(dirname(dream2015.__file__), 
        'code-with-inputdata')

    """ this module calculates the range of cells and drugs from dataset """
    df1 = pd.read_csv(datadir+'/THERAPY_TRAINSET.CSV') 
    df2 = pd.read_csv(datadir+'/THERAPY_TESTSET.CSV')

    cells = set( df1['CELL_LINE'].tolist() + df2['CELL_LINE'].tolist() )
    drugs = set( df1['COMPOUND_A'].tolist() + df2['COMPOUND_B'].tolist() )

    df0 = pd.DataFrame([], columns='CELL_LINE,COMPOUND_A,COMPOUND_B,COMBINATION_ID'.split(','))

    cell_list = [] 
    drug1_list = []
    drug2_list = [] 
    drugcombi = []
    for k,cell in enumerate(cells):
        progressbar.update(k, len(cells))
        for combi in combinations(drugs,2):
            cell_list.append(cell)
            drug1_list.append(combi[0])
            drug2_list.append(combi[1])
            drugcombi.append(".".join(combi))

    df0['CELL_LINE'] = cell_list
    df0['COMPOUND_A'] = drug1_list
    df0['COMPOUND_B'] = drug2_list
    df0['COMBINATION_ID'] = drugcombi

    return df0


def step1():

    outputfile = 'inputdb.csv'
    if exists(outputfile):
        return
    # result1 = get_range()
    result2 = get_inputcombination()
    # result2 = pd.concat([result2 for i in range(10)], ignore_index=True)
    result2.to_csv(outputfile, index=False)


def step2():
    
    outputfile = 'inputdb.csv'
    df = pd.read_csv(outputfile)
    N = df.shape[0]
    STEP = 3000

    df1 = pd.DataFrame([],columns=['inputfile'])
    k = 0
    for i in range(0, N, STEP):
        progressbar.update(i, N) 
        st = i 
        if i + STEP >= N: 
            ed = N - 1
        else: 
            ed = i + STEP - 1
        df0 = df.loc[st : ed]
        #infilename = 'inputdata_%d_%d.csv' % (st, ed)
        infilename = 'inp_part_%d.csv' % (k) 
        #outfilename = 'inputdata_%d_%d_res.csv' % (st, ed)
        df0.to_csv(infilename, index=False)
        #predictor.run_csv(infilename, outfilename, sigma=10)
        df1.loc[k, 'inputfile'] = infilename 
        
        k+=1 

    df1.to_csv('inp_part_list.csv')


def test(): 

    step1()
    step2() 


