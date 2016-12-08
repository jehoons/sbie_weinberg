# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 15:01:33 2016

@author: dwlee
"""
from ipdb import set_trace
import os
import re
import json
import argparse

import numpy as np
import pandas as pd

#if __name__ == '__main__':
#    import sys
#    sys.path.append('sfa')

import sbie_weinberg

import sfa

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-a',
                        '--algorithm',
                        help="Abbreviation of algorithm name (default: SP)")

    parser.add_argument('-c',
                        '--cell-name',
                        help="Name of cell-line to be analyzed")

    parser.add_argument('-d',
                        '--drugs',
                        help="List of drugs (comma separated words)")

    parser.add_argument('-i',
                        '--inputs',
                        help="List of input nodes (comma separated words)")


    args = parser.parse_args()

    p = re.compile(r'^"|"$')

    # Algorithm
    if not args.algorithm:
        ALG = "SP"
    else:
        ALG = p.sub('', args.algorithm.strip())

    # Cell name
    if not args.cell_name:
        raise argparse.ArgumentError("Cell name should be specified")

    CELL_NAME = p.sub('', args.cell_name.strip())


    # Drugs
    if not args.drugs:
        DRUGS = None
    else:
        DRUGS = args.drugs
        if DRUGS:
            DRUGS = p.sub('', DRUGS.strip())
            DRUGS = DRUGS.split(',')
            DRUGS = [drug.strip().upper() for drug in DRUGS]

    # Inputs
    if not args.inputs:
        INPUTS = None
    else:
        INPUTS = args.inputs
        INPUTS = p.sub('', INPUTS.strip())
        INPUTS = INPUTS.split(',')
        INPUTS = [inp.strip() for inp in INPUTS]

    print("Cell name: ", CELL_NAME)
    print("Drugs: ", DRUGS)
    print("Inputs: ", INPUTS)


    return ALG, CELL_NAME, DRUGS, INPUTS


def load_drug_data(fpath, drug_names):
    set_drugs = set(drug_names)
    p = re.compile("sfa_drug_(.+)\.json")
    for fname in os.listdir(fpath):
        m = p.search(fname)
        if m:
            fname_drugs = m.group(1).split('_')
            if set(fname_drugs) == set_drugs:
                with open(os.path.join(fpath, fname), 'r') as fin:
                    return json.load(fin)
        else:
            continue
    # end of for
    raise ValueError("The given drugs are not valid: {}".format(drug_names))


# end of def

def load_cellline_data(fpath, cell_name):
    for fname in os.listdir(fpath):
        if cell_name in fname:
            with open(os.path.join(fpath, fname), 'r') as fin:
                return pd.Series(json.load(fin))
# end of def

def load_input_data(inputs):
    if inputs:
        return {inp:1 for inp in inputs}
    else:
        return {}

def create_basal_activity(N, n2i, cellline_data):
    b = np.zeros((N,), dtype=np.float)
    for name, val in cellline_data.items():
        b[ n2i[name] ] = val

    return b
# end of def


def set_basal_activity(n2v, n2i, b):
    """
    n2v: name to values
    n2i: name to index
    b: basal activity, which is modified in this function.
    """
    if n2v is None:
        return

    for name, val in n2v.items():
        idx = n2i[name]
        b[idx] = val
    # end of for


# Data formatted for SFA
class FumiaData(sfa.base.Data):

    def __init__(self):

        self._abbr = "FUMIA_2013"
        self._name = ""

        dpath = os.path.dirname(__file__)
        dpath_network = os.path.join(dpath, "fumia_network.sif")

        A, n2i, dg = sfa.read_sif(dpath_network, as_nx=True)
        self._A = A
        self._n2i = n2i
        self._dg = dg

        self.i2n = {idx:name for name, idx in self._n2i.items()}
    # end of def
# end of class


def run_sfa(ALG, CELL_NAME, DRUGS, INPUTS, outputfilename):

        # Define the directories of data
    dir_root = os.path.dirname(__file__)
    dir_drug = os.path.join(dir_root, 'drug_data')
    dir_cellline = os.path.join(dir_root, 'cellline_data')


    """
    Load necessary data: drug combination and cell-line info.
    - drug_data is a list of dictionaries
    - cellline_data is pandas.Series
    - input-data is a dictionary

    * The way of creating input_data can be replaced in the future.
    """
    drug_data = load_drug_data(dir_drug, DRUGS)
    cellline_data = load_cellline_data(dir_cellline, CELL_NAME)
    input_data = load_input_data(INPUTS)

    # For testing purpose
    #print("Drug data loaded: ", drug_data)
    #print("Cellline data loaded: ", cellline_data)

    # set_trace()

    """
    Create and apply algorithm to the data
    """
    # Create algorithm object and assign Fumia data
    algs = sfa.AlgorithmSet()
    algs.create(ALG)
    alg = algs[ALG]  # SignalPropagation algorithm object
    data = FumiaData()
    alg.data = data
    alg.initialize(init_data=False)

    # Prepare basal activity vector
    b = create_basal_activity(data.A.shape[0],  # Number of nodes
                              data.n2i,
                              cellline_data)

    ''' 여기서는 GF등과 같은 입력조건을 반영한다 '''
    set_basal_activity(input_data, data.n2i, b)
    set_basal_activity(drug_data, data.n2i, b)
    # set_trace()

    # Perform the calculation of signal propagation algorithm
    x = alg.compute(b)  # x is a vector of stationary state

    # Calcualte flow matrix
    F = alg.W*x

    """
    Prepare result data
    """
    ir, ic = F.nonzero()
    res_sfa = {}

    # Simulation condition
    res_sfa['cell_name'] = CELL_NAME
    res_sfa['drugs'] = drug_data
    res_sfa['inputs'] = input_data
    res_sfa['algorithm'] = ALG

    # Store the result data
    res_sfa['stationary_state'] = {}
    for i, val in enumerate(x):
        name = data.i2n[i]
        res_sfa['stationary_state'][name] = val
    # end of for

    res_sfa['signal_flow'] = []
    for i in range(x.shape[0]):
        isrc, itgt = ic[i], ir[i]
        src = data.i2n[isrc]
        tgt = data.i2n[itgt]
        res_sfa['signal_flow'].append([src, tgt, F[itgt, isrc]])
    # end of for


    # Create a format string for output file
    if DRUGS:
        str_drugs = '+'.join(DRUGS)
    else:
        str_drgus = 'NA'

    if INPUTS:
        str_inputs = '+'.join(INPUTS)
    else:
        str_inputs = 'NA'

    with open(outputfilename, "w") as fout:
        json.dump(res_sfa, fout, indent=4)

    # end of function


def run(inputjson, outputjson):

    with open(inputjson, 'r') as f:
        inputdata = json.load(f)

    drugs = inputdata['input']['drugs']
    drugs = [name.upper() for name in drugs]

    celltype = inputdata['input']['celltype']

    default_alg = 'SP'
    default_ic = ['GFs']

    run_sfa(default_alg, celltype, drugs, default_ic, outputjson)
