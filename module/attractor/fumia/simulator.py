# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************

__all__ = [] 

import os
import sys 
from os.path import dirname,join,abspath,basename
from os import getcwd
from subprocess import call, Popen
from pdb import set_trace
import pandas as pd 
import json 

matlab_root = join(dirname(__file__), 'matlab')


def run(infile, outfile, sample_size=100, time_length=1000):

    infile = abspath(infile)
    outfile = abspath(outfile)
    
    cwd = getcwd()    

    os.chdir(matlab_root)
    
    cmd = 'matlab -r \"fumia_simulator(\'%s\',\'%s\',%d,%d); exit();\"' % \
        (infile, outfile, sample_size, time_length)
    
    os.system(cmd)

    os.chdir(cwd)


def summary(result_json): 

    with open(result_json) as fobj: 
        data = json.load(fobj)

    before = data['output']['before']
    after = data['output']['after']

    df = pd.DataFrame([], columns=['mode', 'phenotype', 'basin'])

    idx = 0
    
    for att in before.keys():
        this = before[att]
        df.loc[idx, 'mode'] = 'before'
        df.loc[idx, 'phenotype'] = this['phenotype']
        df.loc[idx, 'basin'] = this['basin_of_attraction']
        idx += 1

    for att in after.keys():
        this = after[att]
        df.loc[idx, 'mode'] = 'after'
        df.loc[idx, 'phenotype'] = this['phenotype']
        df.loc[idx, 'basin'] = this['basin_of_attraction']
        idx += 1

    for mode in ['before', 'after']:
        num_attrs = df[df['mode']==mode]['mode'].count()
        filt_prolif = (df['mode']==mode) & (df['phenotype'] == 'Proliferation')
        num_attrs_prolif = df.loc[filt_prolif, 'mode'].count()
        
        filt_apopt = (df['mode']==mode) & (df['phenotype'] == 'Apoptosis')
        num_attrs_apopt = df.loc[filt_apopt, 'mode'].count()

        print (mode)
        print (num_attrs)
        print (num_attrs_prolif)
        print (num_attrs_apopt)

        grp = df.groupby(['mode', 'phenotype']).groups

        for g in grp.keys(): 
            print (g)
            idx = grp[g]
            print (df.loc[idx, 'basin'].sum())

    # set_trace()


def visualizer(result_json): 

    # not implemented yet. 
    pass


