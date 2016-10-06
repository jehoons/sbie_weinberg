# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************
__all__ = []

# import urllib 
# import tarfile 
# from urllib import request
# import itertools
# import shutil
# import tempfile
# from os.path import join, isdir

# def download_url(src_url, filename, dst_dir='.', uncompress=False):

#     if not isdir(dst_dir): 
#         assert False

#     # print ('downloading ...')
    
#     _tmpfile = tempfile.mktemp()
#     r = request.urlretrieve(src_url, _tmpfile)
    
#     if uncompress: 
#         zf = tarfile.open(_tmpfile)
#         zf.extractall(dst_dir)
#     else:
#         shutil.copy(_tmpfile, join(dst_dir, filename))

#     print (_tmpfile)


# def test_download_url():

#     src_url = 'https://www.dropbox.com/s/lyn714ff1dzgrk9/my-mails.txt?dl=1'
#     filename = 'my-mails.txt'
#     download_url(src_url, filename, dst_dir='.', uncompress=False)



