# -*- coding: utf-8 -*-
#*************************************************************************
# Author: Je-Hoon Song, <song.jehoon@gmail.com>
# 
# This file is part of {sbie_weinberg}.
#*************************************************************************
import wget 

SYNO="http://143.248.32.25:5000"

# # Username to auth
# USER="jhsong"

# # Password for the above user
# # Possible issue if it contains the & character
# PASS=""

# # Step 1. Retreive API information 
# RESULT=`wget -qO - "$SYNO/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.FileStation" | grep '"success":true'`
# echo $RESULT

# # Step 2. Login
# SID=`wget -qO - "$SYNO/webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account=$USER&passwd=$PASS&session=FileStation&format=cookie" | grep 'sid' | awk -F\" '{print $6}'`
# echo $SID

# # Step 3. Request 
# # RESULT=`wget -qO - "$SYNO/webapi/entry.cgi?api=SYNO.FileStation.Download&_sid=$SID&version=2&method=download&path=%5B%22%2Fhome%2F1.zip%22%5D&mode=%22download%22"`
# # echo $RESULT
# wget -qO downloaded "$SYNO/webapi/entry.cgi?api=SYNO.FileStation.Download&_sid=$SID&version=2&method=download&path=%5B%22%2Fhome%2Flocal%2Fsbie_platform%2Fcode-with-inputdata.tar.gz%22%5D&mode=%22download%22"

# # Ste 4. Logout
# wget -qO - "$SYNO/webapi/auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=FileStation" > /dev/null

# Ref. 
# https://pypi.python.org/pypi/wget
# http://www.w3schools.com/tags/ref_urlencode.asp
# https://global.download.synology.com/download/Document/DeveloperGuide/Synology_File_Station_API_Guide.pdf

