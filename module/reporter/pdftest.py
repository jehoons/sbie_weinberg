import json
import numpy as np
from fpdf import FPDF

def make_pdf(userid, dream_output):
	inputjson = "/data/ui_input/" + str(userid) + "input.json"

	f = open(inputjson,'r')
	js = json.loads(f.read())
	f.close()
	f = open(dream_output,'r')
	output = f.readlines()
	f.close()

	output = output[1:]
	for i in range(len(output)):
		output[i] = output[i].split(',')
		output[i][2] = output[i][2].strip()
	output = np.array(output)
	ce = np.unique(output[:,0])

	so = np.argsort(output[ce[0] == output[:,0],2])
	ran = output[ce[0] == output[:,0],1:3][so]
	ran = ran[-1:-4:-1]

	pdf = FPDF()
	pdf.add_page()
	pdf.set_font('Arial', 'B', 16)
	pdf.cell(0, 10, js['cell_lines'],0,1)
	pdf.cell(0, 10, js['simulation_mode']+'\n'+js['optimal_therapy'],0,1)
	pdf.cell(0, 10, 'Cell line similarity',0,1)
	pdf.image('/data/ui_input/'+str(userid)+'celllines.png',w=200,h=100)
	if js['simulation_mode'] == 'clinical_trial':
		pdf.cell(0, 10, 'Drug similarity',0,1)
		pdf.image('/data/ui_input/'+str(userid)+'drugs.png',w=200,h=100)

	pdf.set_font('Arial', 'B', 20)
	pdf.cell(0,8, 'Dream challenge reference model', 0,1)
	for i in range(len(ce)):
		pdf.set_font('Arial', 'B', 16)
		pdf.cell(0,10, ce[i],0,1)
		pdf.set_font('Arial','',13)
		pdf.cell(0,10, 'Combination    Synergy score',0,1)
		so = np.argsort(output[ce[i] == output[:,0],2].astype(np.float))
		ran = output[ce[i] == output[:,0],1:3][so]
		ran = ran[-1:-4:-1]
		for j in range(len(ran)):
			pdf.cell(0,10, ran[j,0]+'     '+ran[j,1],0,1)


	outfile = '/data/ui_output/' +str(userid) + 'output.pdf'
	pdf.output(outfile, 'F')
