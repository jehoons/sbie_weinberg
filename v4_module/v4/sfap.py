# -*- coding: utf-8 -*-
"""
This module includes utility functions used for
analyses based on SFA on the Platform (SFAP).

author: Daewon Lee (dwl@kaist.ac.kr)
"""

import numpy as np
import sfa
from sfa.vis import compute_graphics

def apply_attributes(key, dict_args, n2i, W, b):
    if key in dict_args:
        for dict_elem in dict_args[key]:            
            value = dict_elem['value']
            attr_type = dict_elem['type']
            if attr_type  == 'node':
                iden = dict_elem['node_id']
                b[n2i[iden]] = value
            elif attr_type == 'link':
                iden_src = dict_elem['source_id']
                iden_tgt = dict_elem['target_id']                
                W[n2i[iden_tgt], n2i[iden_src]] *= value
            else:
                err_msg = "Invalid type for %s: %s"%(key, attr_type)
                raise ValueError(err_msg)


def analyze_perturb_mutations(alg, dict_args):
    # Prepare simulations.
    n2i = alg.data.n2i
    N = len(n2i)    
    b = np.zeros((N,), dtype=np.float)
    W_ctrl = alg.W.copy()    
    
    # Apply the basal activities.
    if 'basal_acts' in dict_args:
        for dict_elem in dict_args['basal_acts']:
            iden = dict_elem['node_id']
            value = dict_elem['value']
            b[n2i[iden]] = value
    
    # Apply the inputs.
    if 'inputs' in dict_args:
        for dict_elem in dict_args['inputs']:
            iden = dict_elem['node_id']
            value = dict_elem['value']
            b[n2i[iden]] = value
    
    # Apply the mutations.
    apply_attributes('mutations', dict_args, n2i, W_ctrl, b)
    
    # Perform the simulation under control condition.
    x_ctrl, trj_ctrl = alg.propagate_iterative(
                                W_ctrl,
                                b,
                                b,
                                a=alg.params.alpha,
                                lim_iter=alg.params.lim_iter)

    # Apply perturbations
    W_pert = W_ctrl.copy()
    apply_attributes('perturbs', dict_args, n2i, W_ctrl, b)
    
    
    for i in b.nonzero()[0]:
        print(i, alg.data.i2n[i], b[i])
    
    # Perform the simulation under perturbation condition.
    alg.W = W_pert
    x_pert, trj_pert = alg.propagate_iterative(
                                W_pert,
                                b,
                                b,
                                a=alg.params.alpha,
                                lim_iter=alg.params.lim_iter)
    
    F = W_pert*x_pert - W_ctrl*x_ctrl
    act = x_pert - x_ctrl
    return F, act
    
def analyze_signal_flow(dict_args):
    # Create data object from SIF file.
    fpath = dict_args['network_id']
    data = sfa.create_from_sif(fpath)
    
    # Create and initialize SP algorithm.
    algs = sfa.AlgorithmSet()
    alg = algs.create('SP')
    alg.data = data
    
    # Set the parameter, alpha
    if 'alpha' in dict_args:
        alg.params.alpha = dict_args['alpha']
    else:
        alg.params.alpha = 0.5
    
    if 'lim_iter' in dict_args:
        alg.params.lim_iter = dict_args['lim_iter']
    else:
        alg.params.lim_iter = 1000
    
    alg.params.apply_weight_norm = True
    alg.initialize()
    F, act = analyze_perturb_mutations(alg, dict_args)
    if not F.any():
        F = data.A
    dg = compute_graphics(F,
                          act,
                          data.A,
                          data.n2i,
                          lw_min=1.0,
                          lw_max=5.0,
                          pct_link=90,
                          pct_act=90)
    return F, act, dg


# Simple unit test using __main__
if __name__ == "__main__":
    input_sfa = {}
    
    input_sfa['network_id'] = 'network.sif'

    input_sfa['inputs'] = []
    input_sfa['inputs'].append({'node_id': 'TGFβ', 'value': 1})
    
    input_sfa['perturbs'] = []
    input_sfa['perturbs'].append({'node_id': 'SMAD',
                                  'type': 'node',
                                  'value': -1})
    
    input_sfa['perturbs'].append({'type': 'link',
                                  'source_id': 'RAS',
                                  'target_id': 'RAF',
                                  'value': 0.1})
    
    input_sfa['mutations'] = []
    input_sfa['mutations'].append({'node_id': 'NOTCH',
                                   'type': 'node', 
                                   'value': 10})
    
    input_sfa['mutations'].append({'type': 'link', 
                                   'source_id': 'Goosecoid',
                                   'target_id': 'TWIST1',
                                   'value': 2})
    
    input_sfa['outputs'] = []
    input_sfa['outputs'].append({'node_id': 'EMT'})
    
    input_sfa['basal_acts'] = []
    input_sfa['basal_acts'].append({'node_id': 'PI3K', 'value': 1})
    input_sfa['basal_acts'].append({'node_id': 'SNAI1', 'value': 0.5})
    
    input_sfa['alpha'] = 0.5
    input_sfa['lim_iter'] = 500
        
    F, act, dg = analyze_signal_flow(input_sfa)

    
