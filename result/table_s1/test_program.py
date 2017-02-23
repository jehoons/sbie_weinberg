# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_weinberg}.
#*************************************************************************
import os
from os.path import dirname, join, exists
import sbie_weinberg
from sbie_weinberg.result import table_s1
import pickle
import json
from ipdb import set_trace
import pandas as pd
from sbie_weinberg.util import progressbar

def labeling(scanning_result, clustering_result, outputfile):
    config = table_s1.get_config()

    num_results = len( scanning_result['scanning_results'] )
    attr_class_list = []
    for i_res, a_result in enumerate(scanning_result['scanning_results']):
        for k in a_result['attractors'].keys():
            attr_type = a_result['attractors'][k]['type']
            if attr_type == 'cyclic':
                class_weight = {}
                cycle_states = a_result['attractors'][k]['value']
                temp_df = pd.DataFrame([], columns=['state', 'class'])
                value_to_class = []
                for i, state_key in enumerate(cycle_states):
                    idxvalue = clustering_result['total_atts_state_key'].tolist().index(state_key)
                    class_type = '%d' % clustering_result['cluster'][idxvalue]
                    value_to_class.append(class_type)
                    if class_type not in class_weight:
                        class_weight[class_type]=1
                    else:
                        class_weight[class_type]+=1

            elif attr_type == 'point':
                class_weight = {}
                idxvalue = clustering_result['total_atts_state_key'].tolist().index(k)
                class_type = '%d' % clustering_result['cluster'][idxvalue]
                value_to_class = class_type
                class_weight[class_type]=1

            class_count = 0
            for class_key in class_weight:
                class_count += class_weight[class_key]

            for class_key in class_weight:
                class_weight[class_key] = float(class_weight[class_key])/float(class_count)

            a_result['attractors'][k]['value_to_class'] = value_to_class
            a_result['attractors'][k]['class_weight'] = class_weight

        attr_class_list.append(a_result)

    with open(outputfile, 'w') as fp:
        json.dump({'scanning_results': attr_class_list}, fp, indent=2)


def test_this(force):
    config = table_s1.get_config()

    if not exists(config['tables']['f']) or force == True:
        print('table f ...')
        labeling(table_s1.load_table('d'), table_s1.load_table('e'), config['tables']['f'])

    if not exists(config['tables']['j']) or force == True:
        print('table j ...')
        labeling(table_s1.load_table('h'), table_s1.load_table('i'), config['tables']['j'])
