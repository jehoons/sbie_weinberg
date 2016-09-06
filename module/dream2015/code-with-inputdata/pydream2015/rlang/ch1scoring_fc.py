# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import os,sys,json
from os.path import join, split as pathsplit, exists

# ch1scoring_fc_r2 is most updated version, and should be used for scoring.  
ch1scoring_fc_r = join(pathsplit(__file__)[0], 'ch1scoring_fc.R')
ch1scoring_fc_r2 = join(pathsplit(__file__)[0], 'ch1scoring_fc2.R')
ch1scoring_fc_r2a = join(pathsplit(__file__)[0], 'ch1scoring_fc2a.R')

ch1scoring_fc_r = os.path.abspath(ch1scoring_fc_r)
ch1scoring_fc_r2 = os.path.abspath(ch1scoring_fc_r2)
ch1scoring_fc_r2a = os.path.abspath(ch1scoring_fc_r2a)


def run(obs, pred, confid, score_json):
    cmd = "Rscript %s %s %s %s %s" % (ch1scoring_fc_r, obs, pred, confid,
            score_json) 
    os.system(cmd)


def run2(obs, pred, confid, score_json, overwrite=False):
    if exists(score_json) and (overwrite==False):
        print ('file already exists:', score_json)
        return 
    else: 
        cmd = "Rscript %s %s %s %s %s" % (ch1scoring_fc_r2, obs, pred, confid,
                score_json) 
        os.system(cmd)


def run2a(obs, pred, score_json, overwrite=False):
    if exists(score_json) and (overwrite==False):
        print ('file already exists:', score_json)
        return 
    else: 
        cmd = "Rscript %s %s %s %s" % (ch1scoring_fc_r2a, obs, pred, score_json) 
        os.system(cmd)


