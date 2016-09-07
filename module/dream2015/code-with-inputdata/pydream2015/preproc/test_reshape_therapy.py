# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import glob
import os
from os.path import join, split as pathsplit
import json
from pdb import set_trace
import pandas as pd
from os.path import exists

import numpy as np
from numpy import corrcoef

# mono-therapy data를 활용하기 위해서, 이 모듈은 주어진 2d 데이터는 1d therapy table로 
# 그 데이터의 모양을 재정리한다.

def test_reshape_therapy(with_small, overwrite, outputfile='therapy_expanded.csv'): 

    overwrite = True 

    if exists(outputfile) and (overwrite==False):
        return 

    import sys
    sys.path.append('..') 

    import pydream2015
    from pydream2015.util import update_progress 

    indir = join(pathsplit(pydream2015.__file__)[0], 'test_input')
    outdir = join(pathsplit(pydream2015.__file__)[0], 'test_output')
    indir = os.path.abspath(indir)
    outdir = os.path.abspath(outdir)
    pydream2015.initdatapath(indir, outdir)

    output_df = pd.DataFrame([], columns=['CELL_LINE', 'COMBINATION_ID', \
            'COMPOUND_A', 'COMPOUND_B', 'DOSE_A', 'DOSE_B', 'UNIT_A', \
            'UNIT_B', 'RESPONSE', 'METHOD', 'FILE_SOURCE'])

    df1 = pd.read_csv(pydream2015.DATA_COMBITHERAPY)

    # 디렉토리 내용가져오기
    raw_data_dir = pydream2015.DIR_TRAINING_COMBI_THERAPY

    files = glob.glob(join(raw_data_dir, '*.csv'))

    idx = 0 

    for kk, thisfile in enumerate(files):
        update_progress(kk, len(files))
        filedata = pd.read_csv(thisfile, index_col='Unnamed: 0') 

        dim_agent_1 = filedata.index.values.tolist().index('(=Agent 1)')
        dim_agent_2 = filedata.columns.values.tolist().index('(=Agent 2)')
        agent2_doses = filedata.columns.values.tolist()[0:dim_agent_2]
        agent1_doses = filedata.index.values.tolist()[0:dim_agent_1]

        lbl_agent_1 = filedata.loc['Agent1', agent2_doses[0]]
        lbl_agent_2 = filedata.loc['Agent2', agent2_doses[0]]
        unit_1 = filedata.loc['Unit1', agent2_doses[0]]
        unit_2 = filedata.loc['Unit2', agent2_doses[0]]
        title = filedata.loc['Title', agent2_doses[0]]
        
        for agent1 in agent1_doses:
            for agent2 in agent2_doses: 
                response = filedata.loc[agent1, agent2] 
                output_df.loc[idx, 'CELL_LINE'] = title 
                output_df.loc[idx, 'COMBINATION_ID'] = lbl_agent_1 + '.' + lbl_agent_2
                output_df.loc[idx, 'COMPOUND_A'] = lbl_agent_1
                output_df.loc[idx, 'COMPOUND_B'] = lbl_agent_2
                output_df.loc[idx, 'DOSE_A'] = agent1
                output_df.loc[idx, 'DOSE_B'] = agent2
                output_df.loc[idx, 'UNIT_A'] = unit_1
                output_df.loc[idx, 'UNIT_B'] = unit_2
                output_df.loc[idx, 'RESPONSE'] = response
                
                if (agent1 == "0") and (agent2 == "0"):
                    output_df.loc[idx, 'METHOD'] = 'CONTROL'
                elif (agent1 == "0") or (agent2 == "0"):
                    output_df.loc[idx, 'METHOD'] = 'MONO'
                else: 
                    output_df.loc[idx, 'METHOD'] = 'COMBI'

                output_df.loc[idx, 'FILE_SOURCE'] = os.path.split(thisfile)[1]

                idx += 1
        
    output_df.to_csv('therapy_expanded.csv', index=False )
    
