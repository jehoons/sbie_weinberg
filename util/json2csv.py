import json
import csv

def json2csv_combi(userid):
	inputjson = "/data/ui_input/" + str(userid) + "input.json"
	f = open(inputjson,'r')
	js = json.loads(f.read())
	f.close()
	
	outpath = "/data/ui_input/dream/" + str(userid) + "input.csv"
	outfile = open(outpath,'w')
	writer = csv.writer(outfile)
	header = ['CELL_LINE','COMPOUND_A','COMPOUND_B','COMBINATION_ID']
	writer.writerow(header)
	
	cells = js['cell_lines'].split(',')
	drugs = js['drugs'].split(',')
	
	for i in range(len(drugs)):
		temp = drugs[i].split('_')[1:]
		temp2 = temp[0]
		if len(temp) > 1:
			for j in range(1,len(temp)):
				temp2 = temp2 + '_' + temp[j]
		drugs[i] = temp2

	if len(drugs) > 1:
		for i in range(len(cells)):
			for j in range(len(drugs)-1):
				for k in range(j+1,len(drugs)):
					line = [cells[i], drugs[j], drugs[k], drugs[j]+'.'+drugs[k]]
					writer.writerow(line)
	elif len(drugs) == 1:
		for i in range(len(cells)):
			line = [cells[i], drugs[0], drugs[0], drugs[0]+'.'+drugs[0]]
			writer.writerow(line)

	outfile.close()

def json2csv_optimal(userid):
	inputjson = "/data/ui_input/" + str(userid) + "input.json"
	f = open(inputjson,'r')
	js = json.loads(f.read())
	f.close()


	outpath = "/data/ui_input/dream/" + str(userid) + "input.csv"
	outfile = open(outpath,'w')
	writer = csv.writer(outfile)
	header = ['CELL_LINE','COMPOUND_A','COMPOUND_B','COMBINATION_ID']
	writer.writerow(header)

	cells = js['cell_lines'].split(',')
	drugs = []

	f = open("/data/platform/db/drug_info_sbie_full.csv",'r')
	data = f.readlines()
	for i in range(1,len(data)):
		drugs.append(data[i].split(',')[0])
	f.close()

	for i in range(len(drugs)):
		temp = drugs[i].split('_')[1:]
		temp2 = temp[0]
		if len(temp) > 1:
			for j in range(1,len(temp)):
				temp2 = temp2 + '_' + temp[j]
		drugs[i] = temp2
	if len(drugs) > 1:
		for i in range(len(cells)):
			for j in range(len(drugs)-1):
				for k in range(j+1,len(drugs)):
					line = [cells[i], drugs[j], drugs[k], drugs[j]+'.'+drugs[k]]
					writer.writerow(line)

	outfile.close()

