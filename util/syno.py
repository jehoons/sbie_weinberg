# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************
import wget 
from pdb import set_trace
import json
import urllib
from os.path import basename,join
import os 


def download(SYNO, SOURCE, TARGET_DIR, USER, PASS):

    # Step 1. Login

    url = "%s/webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account=%s&passwd=%s&session=FileStation&format=cookie" % (SYNO, USER, PASS)

    filename = wget.download(url)

    with open(filename, 'r') as f: 
        data = json.load(f)
    
    os.system('rm -f %s' % (os.path.abspath(filename)))

    SID = data['data']['sid']

    # Step 2. Request

    PATH = urllib.parse.quote_plus( "[\"%s\"]" % SOURCE )    

    MODE = urllib.parse.quote_plus( "\"download\"" )

    url = "%s/webapi/entry.cgi?api=SYNO.FileStation.Download&_sid=%s&version=2&method=download&path=%s&mode=%s" % (SYNO, SID, PATH, MODE)

    filename = wget.download(url)
    
    wget.shutil.move(filename, join(TARGET_DIR, basename(SOURCE)))

    # Step 3. Logout

    url = "%s/webapi/auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=FileStation" % SYNO
    
    filename = wget.download(url)
    
    os.system('rm -f %s' % (os.path.abspath(filename)))




# The command-line version of this code can be written based on following code: 

# #!/bin/bash
# # Editor: Je-Hoon Song, song.jehoon@gmail.com
# # Original code is copied from git@github.com:mb243/SynoDL.git. 

# # Shortcomings:
# # This script is based on the Synology Download Station V3 API published at
# # http://download.synology.com/download/other/Synology_Download_Station_Official_API_V3.pdf
# # but does not take some of it's recommendations, specifically that of checking the location
# # of APIs from the query. It assumes these APIs are in fixed locations.

# # URL of the Syno including HTTP port for API authentication.
# # No trailing slash
# SYNO="http://143.248.32.25:5000"

# # Username to auth
# USER="jhsong"

# # Password for the above user
# # Possible issue if it contains the & character
# PASS="0909room"

# # File to parse URLs from
# # Each URL should be on a seperate line
# # Possible issue if it contains the & character
# FILE="./urls.txt"

# # Verify API with DM
# echo -n "Verifying API ... "
# RESULT=`wget -qO - "$SYNO/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.DownloadStation.Task" | grep '"success":true'`

# if [ "$RESULT" != "" ]
# then
#     echo "ok"
#     # Authenticate to DM
#     echo -n "Authenticating to API ... "
#     SID=`wget -qO - "$SYNO/webapi/auth.cgi?api=SYNO.API.Auth&version=2&method=login&account=$USER&passwd=$PASS&session=DownloadStation&format=sid" | grep 'sid' | awk -F\" '{print $6}'`
#     if [ "$SID" != "" ]
#     then
#         echo "ok"
#         # Session ID obtained in SID
#         # Start parsing the file list
#         while read line
#         do
#             echo $line
#             # a line has been read in as $line            
#             # send this to the Syno DM
#             echo -n "Sending task to DM: $line ... "
#             RESULT=`wget -qO - --post-data "api=SYNO.DownloadStation.Task&version=1&method=create&uri=$line&_sid=$SID" "$SYNO/webapi/DownloadStation/task.cgi" grep '"success":true'`
#             # $echo $RESULT            
#             if [ "$RESULT" != "" ]
#             then
#                 echo "ok"
#             else
#                 echo "fail"
#             fi
#         done < $FILE
#         # Done. Log out (invalidate SID)
#         # Note: Since logging out, don't really care to check the response.
#         echo -n "Logging out of API ... "
#         wget -qO - "$SYNO/webapi/auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=DownloadStation" > /dev/null
#         echo "done."
#     else
#         echo "fail"
#     fi
# else
#     echo "fail"
# fi




# Ref. 
# https://pypi.python.org/pypi/wget
# http://www.w3schools.com/tags/ref_urlencode.asp
# https://global.download.synology.com/download/Document/DeveloperGuide/Synology_File_Station_API_Guide.pdf

