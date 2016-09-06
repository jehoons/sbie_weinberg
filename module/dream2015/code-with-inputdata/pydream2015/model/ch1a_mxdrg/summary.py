import json
import glob 
import pandas as pd
from pdb import set_trace

def test_summary():

    files = glob.glob('output*.json')

    df1 = pd.DataFrame([])
    for f in files:
        jsondata = json.load(open(f))
        num_coefs = jsondata['model']['shortly']['num_coefs']
        final = jsondata['global_score']['final']
        score = jsondata['global_score']['score']
        tiebreak = jsondata['global_score']['tiebreak']
        df1.loc[f, 'num_coefs'] = num_coefs
        df1.loc[f, 'final'] = final
        df1.loc[f, 'score'] = score
        df1.loc[f, 'tiebreak'] = tiebreak

    df1.to_csv('summary.csv')

    pass
