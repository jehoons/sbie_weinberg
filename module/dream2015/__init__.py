# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************

__all__ = [] 

from os.path import exists, dirname, join, abspath
from urllib import request
import tempfile, tarfile, shutil

import pdb

from sbie_weinberg.util import download_url

""" code-with-inputdata.tar.gz file will be downloaded. 
if code-with-inputdata.tar.gz file is updated, then it will be downloaded again. 
REVISION.txt will record revision number of the file. """ 

revision_url = 'https://www.dropbox.com/s/acuee91q13c8eh7/REVISION.txt?dl=1'
src_url = 'https://www.dropbox.com/s/ywet8d6qk65qgml/code-with-inputdata.tar.gz?dl=1'    


thisdir = abspath(dirname(__file__))

revision_file_1 = join(thisdir, 'REVISION.txt')

revision_file_2 = tempfile.mktemp()

res = request.urlretrieve(revision_url, revision_file_2)

# check version in server side

try:
    with open(revision_file_2, 'r') as f: 
        revision_number_2 = int(f.read())

except ValueError: 
    revision_number_2 = -1

# check version in local machine 

try: 
    with open(revision_file_1, 'r') as f: 
        revision_number_1 = int(f.read())

except FileNotFoundError: 
    revision_number_1 = -1 


if revision_number_2 > revision_number_1: 

    print('downloading dream2015 module ...')

    __tmpfilename = tempfile.mktemp()    
    res = request.urlretrieve(src_url, __tmpfilename)    
    zf = tarfile.open(__tmpfilename)    
    zf.extractall(thisdir)

    # revision_file_2 (from server) is copied into revision_file_1 (local)
    shutil.copyfile(revision_file_2, revision_file_1)

else:
    #print ('local reversion(%d) == server reversion(%d)' % (revision_number_1, 
    #    revision_number_2))
    pass 


def test_this():
    from sbie_weinberg.module import dream2015 
    
