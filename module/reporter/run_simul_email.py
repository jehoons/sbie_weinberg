import os 
import sys
#import time
import json
from fpdf import FPDF
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders

import pdftest
import json2csv

email = sys.argv[1]
userid = sys.argv[2]

inputjson = "/data/ui_input/" + str(userid) + "input.json"
f = open(inputjson,'r')
js = json.loads(f.read())
f.close()

########Make cell, drug similarity image
cells = js['cell_lines']
drugs = js['drugs']
os.system("Rscript /data/platform_scripts/R/draw_cell_similarity.R "+ cells + " " + str(userid))
if js['simulation_mode'] == 'clinical_trial':
	os.system("Rscript /data/platform_scripts/R/draw_drug_similarity.R "+ drugs + " " + str(userid))

######################################


#########Dream Simulation##############
if js['simulation_mode'] == 'clinical_trial':
	json2csv.json2csv_combi(userid)
elif js['simulation_mode'] == 'optimal_therapy':
	json2csv.json2csv_optimal(userid)
inputcsv = "/data/ui_input/dream/" +str(userid) + "input.csv"
outputcsv = "/data/ui_output/dream/" + str(userid) + "output.csv"
#prevdir = os.getcwd()
#os.chdir('/data/platform/dream2015/code-with-inputdata/')
status = os.system('python /data/platform_scripts/models/dream2015/code-with-inputdata/model_prediction.py '+ inputcsv + " " + outputcsv + " " + str(userid))
#os.chdir(prevdir)
#######################################

#Make output pdf file
pdftest.make_pdf(userid, outputcsv)

#Set up crap for the attachments
files = "/data/ui_output/"+ str(userid) + "output.pdf"


#Set up users for email
gmail_user = "rnrcortest@gmail.com"
gmail_pwd = "xptmxm123"
#recipients = ['hanyh0807@naver.com']
recipients = [email]

#Create Module
def mail(to, subject, text, attach):
		msg = MIMEMultipart()
		msg['From'] = gmail_user
		msg['To'] = ", ".join(recipients)
		msg['Subject'] = subject

		msg.attach(MIMEText(text))

#get all the attachments
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(files, 'rb').read())
		Encoders.encode_base64(part)
		nn = 'Result_File.pdf'
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % nn)
		msg.attach(part)

		mailServer = smtplib.SMTP_SSL("smtp.gmail.com", 465)
#mailServer.ehlo()
#mailServer.starttls()
#mailServer.ehlo()
		mailServer.login(gmail_user, gmail_pwd)
		mailServer.sendmail(gmail_user, to, msg.as_string())
# Should be mailServer.quit(), but that crashes...
		mailServer.close()

#time.sleep(60)
#send it
if status == 0:
	mail(recipients,"Result report","Result report",files)
else:
	mail(recipients,"nonono","nonono")
