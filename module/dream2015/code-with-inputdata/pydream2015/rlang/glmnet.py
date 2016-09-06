# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import os,sys,json
from os.path import join, split as pathsplit

glmnet_r = join(pathsplit(__file__)[0], 'glmnet.r')
glmnet_r = os.path.abspath(glmnet_r)

glmnet2_r = join(pathsplit(__file__)[0], 'glmnet2.r')
glmnet2_r = os.path.abspath(glmnet2_r)


def run(input_json, output_json):
    cmd = "Rscript %s %s %s" % (glmnet_r, input_json, output_json) 
    os.system(cmd)


def run2(input_json, output_json):
    cmd = "Rscript %s %s %s" % (glmnet2_r, input_json, output_json) 
    os.system(cmd)


def make_input(xDatafile, yDatafile, glmnet_inputfile, ncores=10, threshold=1000, 
        train_ratio=0.6, alpha=1.0, nfolds=10, nrepeats=3, figure=True, 
        figurefile='output.eps', normalize=False):

    lassconf = { 
            "data": { 
                "xdatafile": xDatafile, 
                "ydatafile": yDatafile, 
                }, 
            "config": { 
                "ncores": ncores, 
                "threshold": threshold, 
                "train_ratio": train_ratio, 
                "alpha": alpha, 
                "nfolds": nfolds, 
                "nrepeats": nrepeats, 
                "figure": figure, 
                "figure_file": figurefile, 
                "normalize": normalize, 
                } 
            }

    fobj = open(glmnet_inputfile, 'wb')
    json.dump(lassconf, fobj, separators=(',',':'), sort_keys=True, indent=2) 
    fobj.write('\n') 
    fobj.close()
    pass 
