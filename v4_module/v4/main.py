import sys
import json

import pymysql
import numpy as np
import pandas as pd

from sfa_wrapper import SFA_sim

# php에서 방금 입력받은 환자의 db id
#patient_id = sys.argv[1]
patient_id = 99

db = pymysql.connect(user='root', passwd='sbl4365', db='v4', charset='utf8')
cursor = db.cursor()

sql = "SELECT * FROM PATIENT WHERE ID=%s"
cursor.execute(sql, patient_id)

patient = cursor.fetchall()


# Network node & gene id mapping
sql = "SELECT NODE_ID, GENE_ID FROM GENE_NODE_MAP WHERE CANCER_ID=%s"
cursor.execute(sql, patient[0][2])

gene_node_map = pd.DataFrame(list(cursor.fetchall()), columns=['node','gene_id'])

# Get mutations of patient
sql = "SELECT GENE_ID, MUTATIONTYPE_ID FROM MUTATION WHERE PATIENT_ID=%s"
cursor.execute(sql, patient_id) 

mutations = pd.DataFrame(list(cursor.fetchall()), columns=['gene_id', 'mutationtype'])

# Extract genes that exist in both network and mutations
intersect_gene = pd.DataFrame(np.intersect1d(gene_node_map['gene_id'].values, mutations['gene_id'].values), columns=['gene_id'])
intersect_gene_name = pd.merge(gene_node_map, intersect_gene, how='inner', on=['gene_id'])
intersect_gene_name = intersect_gene_name['node'].values


patient_input = {}
patient_input['cancer_id'] = patient[0][2]

patient_input['mutations'] = []
for i in range(len(intersect_gene_name)):
    patient_input['mutations'].append({'node_id':intersect_gene_name[i], 'value':1, 'type':'node'})

patient_input['inputs'] = []
patient_input['outputs'] = []
network = {}
if patient[0][2] == 1:  # Breast cancer input & output
    pass
    patient_input['inputs'].append({'node_id': 'DNA_damage', 'value': 1})
    patient_input['inputs'].append({'node_id': 'EGF', 'value': 1})
    patient_input['inputs'].append({'node_id': 'ER', 'value': 1})
    #patient_input['outputs'].append({})
    network['cancer_id'] = 1
    network['logic'] = '/data/networks/BREAST/BREAST_logic.txt'
    network['phenotype_rule'] = '/data/networks/BREAST/BREAST_phenotype.txt'
    network['resistance_score_rule'] = '/data/networks/BREAST/BREAST_resistance_score.txt'
    network['sif'] = '/data/networks/BREAST/BREAST.sif'
    network['sif_'] = '/data/networks/BREAST/BREAST_.sif'
    
elif patient[0][2] == 2:    # Colorectal cancer input & output
    pass
    patient_input['inputs'].append({'node_id': 'EGF', 'value': 1})
    patient_input['inputs'].append({'node_id': 'DNA_damage', 'value': 1})
    patient_input['inputs'].append({'node_id': 'WNT', 'value': 1})
    patient_input['inputs'].append({'node_id': 'TGF_beta', 'value': 1})
    #patient_input['outputs'].append({})
    network['cancer_id'] = 2
    network['logic'] = '/data/networks/COAD/'
    network['phenotype_rule'] = '/data/networks/COAD/COAD_phenotype.txt'
    network['resistance_score_rule'] = '/data/networks/COAD/COAD_resistance_score.txt'
    network['sif'] = '/data/networks/COAD/COAD.sif'
    network['sif_'] = '/data/networks/COAD/COAD_.sif'
elif patient[0][2] == 3:    # Lung cancer input & output
    pass
    patient_input['inputs'].append({'node_id': 'EGFR_stimulus', 'value': 1})
    patient_input['inputs'].append({'node_id': 'PDGFR_stimulus', 'value': 1})
    patient_input['inputs'].append({'node_id': 'CMET_stimulus', 'value': 1})
    patient_input['inputs'].append({'node_id': 'FGFR_stimulus', 'value': 1})
    patient_input['inputs'].append({'node_id': 'TGFBR_stimulus', 'value': 1})
    patient_input['inputs'].append({'node_id': 'DNA_damage', 'value': 1})
    #patient_input['outputs'].append({})
    network['cancer_id'] = 3
    network['logic'] = '/data/networks/LUNG/'
    network['phenotype_rule'] = '/data/networks/LUNG/LUNG_phenotype.txt'
    network['resistance_score_rule'] = '/data/networks/LUNG/LUNG_resistance_score.txt'
    network['sif'] = '/data/networks/LUNG/LUNG.sif'
    network['sif_'] = '/data/networks/LUNG/LUNG_.sif'


sql = "SELECT DRUG_ID1, DRUG_ID2, DRUG_ID3, COUNT FROM TREATMENT"
cursor.execute(sql)

treatment = pd.DataFrame(list(cursor.fetchall()), columns=['drug_id1','drug_id2','drug_id3','count'])
treatment = treatment.values

# Parallel
#for i in range(treatment.shape[0]):
for i in range(3,5):
    sim_input = patient_input.copy()
    #SELECT SYMBOL FROM GENE WHERE ID in (SELECT GENE_ID FROM DRUG_TARGET WHERE DRUG_ID=%s)
    #select NODE_ID from GENE_NODE_MAP where GENE_ID in (select GENE_ID from DRUG_TARGET where DRUG_ID=%s)
    if treatment[i,3] == 1:
        sql = 'select DISTINCT NODE_ID from GENE_NODE_MAP where GENE_ID in (select GENE_ID from DRUG_TARGET where DRUG_ID in (%s))'
        cursor.execute(sql, (int(treatment[i,0])))
    if treatment[i,3] == 2:
        sql = 'select DISTINCT NODE_ID from GENE_NODE_MAP where GENE_ID in (select GENE_ID from DRUG_TARGET where DRUG_ID in (%s, %s))'
        cursor.execute(sql, (int(treatment[i,0]), int(treatment[i,1])))
    if treatment[i,3] == 3:
        sql = 'select DISTINCT NODE_ID from GENE_NODE_MAP where GENE_ID in (select GENE_ID from DRUG_TARGET where DRUG_ID in (%s, %s, %s))'
        cursor.execute(sql, (int(treatment[i,0]), int(treatment[i,1]), int(treatment[i,2])))

    drug_targets = cursor.fetchall()
    sim_input['perturb_targets'] = []
    for dt in drug_targets:
        sim_input['perturb_targets'].append({'node_id':dt[0], 'type':'node', 'value':-1})
    sim_input['network_id'] = network['sif_']
    sim_input['patient_id'] = patient_id
    sim_input['treatment_id'] = i+1
    
    SFA_sim(sim_input)
    #exec('Rscript asdf.r ' + json.dumps(patient_input) + ' ' + json.dumps(model_input) + ' ' + json.dumps(sim_input))

sql = 'update ANALYSIS set STATUS=1 where PATIENT_ID=%s'
cursor.execute(sql, patient_id)
db.commit()
db.close()
