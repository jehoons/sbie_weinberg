import pandas as pd 
from ipdb import set_trace

def test_1(): 

	HALLMARK_APOPTOSIS = 'dataset/MSigDB/HALLMARK_APOPTOSIS.txt'
	HALLMARK_E2F_TARGETS = 'dataset/MSigDB/HALLMARK_E2F_TARGETS.txt'
	HALLMARK_G2M_CHECKPOINT = 'dataset/MSigDB/HALLMARK_G2M_CHECKPOINT.txt'
	HALLMARK_MITOTIC_SPINDLE = 'dataset/MSigDB/HALLMARK_MITOTIC_SPINDLE.txt'
	HALLMARK_MYC_TARGETS_V1 = 'dataset/MSigDB/HALLMARK_MYC_TARGETS_V1.txt'
	HALLMARK_MYC_TARGETS_V2 = 'dataset/MSigDB/HALLMARK_MYC_TARGETS_V2.txt'
	HALLMARK_P53_PATHWAY = 'dataset/MSigDB/HALLMARK_P53_PATHWAY.txt'
	
	fumia_node_list = 'dataset/fumia-node-list.txt'

	df_apo = pd.read_csv(HALLMARK_APOPTOSIS, skiprows=[1])
	df_ef2 = pd.read_csv(HALLMARK_E2F_TARGETS, skiprows=[1])
	df_g2m = pd.read_csv(HALLMARK_G2M_CHECKPOINT, skiprows=[1])
	df_mit = pd.read_csv(HALLMARK_MITOTIC_SPINDLE, skiprows=[1])
	df_myc1 = pd.read_csv(HALLMARK_MYC_TARGETS_V1, skiprows=[1])
	df_myc2 = pd.read_csv(HALLMARK_MYC_TARGETS_V2, skiprows=[1])
	df_p53 = pd.read_csv(HALLMARK_P53_PATHWAY, skiprows=[1])

	hallmarks = set() 

	hallmarks= hallmarks.union( set(df_apo['HALLMARK_APOPTOSIS'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_ef2['HALLMARK_E2F_TARGETS'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_g2m['HALLMARK_G2M_CHECKPOINT'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_mit['HALLMARK_MITOTIC_SPINDLE'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_myc1['HALLMARK_MYC_TARGETS_V1'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_myc2['HALLMARK_MYC_TARGETS_V2'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_p53['HALLMARK_P53_PATHWAY'].values.tolist()) )

	df_fumia = pd.read_csv(fumia_node_list, names=['fumia_node'])
	fumia_nodes = set(df_fumia['fumia_node'].values.tolist())

	print('hallmarks: ', len(hallmarks))
	print('fumia_nodes: ', len(fumia_nodes))
	print('intersection: ', len(fumia_nodes.intersection(hallmarks)))

	set_trace()

