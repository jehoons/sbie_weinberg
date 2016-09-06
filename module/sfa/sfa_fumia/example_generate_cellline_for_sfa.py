# -*- coding: utf-8 -*-
import json
import pandas as pd

# DataFrame containing mutation information
df_muts = pd.read_csv("mutations_labeled.csv",
                      index_col=0)


for cellline in df_muts.columns:
    fname = "cellline_data/sfa_cellline_%s.json"%(cellline)
    print(fname)
    with open(fname, "w") as fin:
        idx_nz = df_muts[cellline].nonzero()[0]
        df_muts[cellline][idx_nz].to_json(fin)
    # end of with