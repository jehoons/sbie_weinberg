from os.path import join, split, exists
from pdb import set_trace
import pdb
import json
import tempfile
import urllib 
import tarfile 
from urllib import request
import re
import itertools
from pyeda.inter import *
from sympy import And, Or, Not, symbols

data_url = 'https://www.dropbox.com/s/pixt23cx3a4yuu4/untracked.tar.gz?dl=1'


def download_untracked():
    savedatafile = tempfile.mktemp()            
    print ('dataset downloading ...')

    r = request.urlretrieve(data_url, savedatafile)
    # open(savedatafile , 'wb').write(r.content)
    zf = tarfile.open(savedatafile)
    zf.extractall('.')


def load_helikar2008():
    if not exists('untracked'):
        download_untracked()

    helikar2008json = 'untracked/result/helikar2008.json'
    helijar2008dict = json.load(open(helikar2008json,'r'))

    # preprocessing 
    for inp in helijar2008dict['input_list']:
        d = helijar2008dict['input_list'][inp]
        if d == None: 
            helijar2008dict['input_list'][inp] = []
        elif type(d) != list: 
            helijar2008dict['input_list'][inp] = []

    for inp in helijar2008dict['logic_list']:
        d = helijar2008dict['logic_list'][inp]
        if d == None: 
            helijar2008dict['logic_list'][inp] = []
        elif type(d) != list: 
            helijar2008dict['logic_list'][inp] = []

    return helijar2008dict


def load_helikar2008_boolean2():

    from infoproc.dataset import load_helikar2008

    data = load_helikar2008()

    variables = [] 
    n_variables = len(data['node_list'].keys())

    for i in range(1, 1+n_variables): 
        idx = 'i%d'%i
        variables.append( data['node_list'][idx] )

    initials = [] 

    for idx in data['node_list']:
        initials.append( data['node_list'][idx] + '= Random' ) 

    # logic_list start index: 1 
    functions = [] 
    for i in range(1, 1 + len(data['logic_list'])):
        idx = 'i%d'%i        
        tt_f_2d = data['logic_list'][idx]
        tt_f_1d = list(itertools.chain(*tt_f_2d))
        tt_f_1d_str = ['%d' % f for f in tt_f_1d]
        inps = data['input_list'][idx]
        num_input = len(inps)

        if num_input > 0 : 
            tt_f = truthtable(ttvars('x', num_input), "".join(tt_f_1d_str))
            f_minimized = espresso_tts(tt_f)
            str_f_min = repr(f_minimized[0])
            for i in range(len(variables)): 
                str_f_min = str_f_min.replace('x[%d]'%(len(variables)-1-i), \
                    variables[i])

            for var in variables:
                cmd = '%s = symbols(\'%s\')' % (var, var)
                exec(cmd)
                
            from sympy import And, Or, Not, Xor, printing 
            cstr = repr( eval('printing.ccode(%s)' % str_f_min) )
            cstr = cstr.replace('&&', 'and')
            cstr = cstr.replace('||', 'or')
            cstr = cstr.replace('!', 'not ')
            cstr = cstr.replace('\'', '')
            functions.append(  data['node_list'][idx] + '*=' + cstr )

    return initials, functions


def test_load_helikar2008_boolean2():
    
    ini, func = load_helikar2008_boolean2()

    # print("\n".join(ini))
    # print("\n".join(func))

    savedatafile = 'model.txt'

    print ('output:', savedatafile)

    open(savedatafile , 'w').write("\n".join(ini+func))
