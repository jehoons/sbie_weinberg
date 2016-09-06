# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
import os,sys
import pandas as pd, numpy as np 
from sets import Set
from os.path import join,exists,split as pathsplit
from os import remove 

import cPickle as pickle 
import pytest

from ..util import update_progress

from pdb import set_trace

def test_calc_dd3d():
    sys.path.append('../..')
    import pydream2015
    from pydream2015 import feature 
    pydream2015.initdatapath('../test_input', '../test_output')

    in_dd3d = pydream2015.DATA_DRUG_DESC_3D
    out_dd3d_conv = pydream2015.MYDATA_DRUG_DESC_3D_CONV

    if not exists(out_dd3d_conv):
        feature.calc_dd3d(in_dd3d, out_dd3d_conv) 
    else: 
        print '>>', out_dd3d_conv, '- skipped'
        

