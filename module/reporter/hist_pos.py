import pytest
import matplotlib
matplotlib.rcParams.update({'font.family': 'Bitstream Vera Sans'})
matplotlib.use('Agg')
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from pdb import set_trace
from os.path import join


def hist_pos(dream2015_therapy, synergy_score, drug, outputfile):	
    df_synergy = pd.read_csv(dream2015_therapy)
    syn = df_synergy['SYNERGY_SCORE']
    fig = plt.figure()
    plt.hist(syn, synergy_score)
    plt.axvline(synergy_score, color='r', linestyle='dashed', linewidth=4)
    ax = fig.add_subplot(111)
    ax.text(synergy_score, 450, drug)
    ax.set_xlabel('synergy score')
    ax.set_ylabel('frequency')
    plt.savefig(outputfile, dpi=600)


dream2015_therapy = 'pydream2015/test_input/dream2015/synergy/ch1_train_combination_and_monoTherapy_updated.csv'
drug_label = 'ABC'
drug_score = 100 
outputfile = 'histpos.png'
hist_pos(dream2015_therapy, drug_score, drug_label, outputfile)
