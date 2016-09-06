# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 14:19:27 2016

@author: dwlee
"""


import json
import itertools

drug_combs = [
    {'drug': 'RAF265', 'target': 'RAF'},
    {'drug': 'Nutlin-3'	, 'target':'MDM2'},
    {'drug': 'AZD6244'	, 'target':'MEK'},
    {'drug': 'ERLOTINIB'  , 'target':'EGFR'} ]

for num_drugs in range(1, 3):
    iter_drug_comb = itertools.combinations(drug_combs, num_drugs)
    for comb in iter_drug_comb:
        list_drugs = '_'.join([drug['drug'].upper() for drug in comb])
        fname = "drug_data/sfa_drug_%s.json"%(list_drugs)
        print(fname)
        with open(fname, "w") as fin:
            list_comb = list(comb)
            json.dump(list_comb, fin)
        # end of with
    # end of for
# end of for
	
	
