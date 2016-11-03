"""
Insert attractor result json file to DB

SELECT query example

 - input state : 00000, target1 : S_Gli, target1 state : 0, target2 : NULL, target2 state : 0
SELECT attractors, state_key FROM attractor WHERE input_nodes='00000' and COLUMN_GET(target1, 'target1' as char)='S_Gli' and COLUMN_GET(target1, 'target1_state' as char)='0' and COLUMN_GET(target2,'target2' as char)='' and COLUMN_GET(target2, 'target2_state' as char)='0';

 - control
SELECT attractors, state_key FROM attractor WHERE input_nodes='00000' and COLUMN_GET(target1, 'target1' as char)='' and COLUMN_GET(target1, 'target1_state' as char)='0' and COLUMN_GET(target2,'target2' as char)='' and COLUMN_GET(target2, 'target2_state' as char)='0';
"""
import json
import pymysql

f = open('/data/TABLE_S7D_SCANNING_RESULT.json','r')
result = json.load(f)
f.close()
result = result["scanning_results"]

f = open('/data/TABLE_S7C_INPUT_COMBINATIONS.json','r')
inputcom = json.load(f)
f.close()

total_record = inputcom['num_configs']
inputcom = inputcom['configs']

inn = ['S_Mutagen', 'S_GFs', 'S_Nutrients', 'S_TNFalpha', 'S_Hypoxia']

db = pymysql.connect(user='root', passwd='sbl4365', db='weinberg')
cursor = db.cursor()

for i in range(total_record):
    step = inputcom[i]['parameters']['steps']
    sample_num = inputcom[i]['parameters']['samples']
    input_nodes = ''
    for j in range(len(inn)):
        if inn[j] in inputcom[i]['parameters']['off_states']:
            input_nodes += '0' 
        elif inn[j] in inputcom[i]['parameters']['on_states']:
            input_nodes += '1'
    target1 = ''; target1_state = 0
    target2 = ''; target2_state = 0
    counter = 0
    for j in range(len(inputcom[i]['parameters']['off_states'])):
        if inputcom[i]['parameters']['off_states'][j] not in inn:
            if counter == 0:
                target1 = inputcom[i]['parameters']['off_states'][j]
                target1_state = 0
                counter += 1
            elif counter == 1:
                target2 = inputcom[i]['parameters']['off_states'][j]
                target2_state = 0
                counter += 1
    for j in range(len(inputcom[i]['parameters']['on_states'])):
        if inputcom[i]['parameters']['on_states'][j] not in inn:
            if counter == 0:
                target1 = inputcom[i]['parameters']['on_states'][j]
                target1_state = 1
                counter += 1
            elif counter == 1:
                target2 = inputcom[i]['parameters']['on_states'][j]
                target2_state = 1
                counter += 1
    attractors = json.dumps(result[i]['attractors'])
    state_key = json.dumps(result[i]['state_key'])
    suc = cursor.execute("INSERT INTO attractor(step, sample_num, input_nodes, target1, target2, attractors, state_key) VALUES (%s, %s, %s, COLUMN_CREATE('target1',%s,'target1_state',%s),COLUMN_CREATE('target2',%s,'target2_state',%s),%s,%s)", (step, sample_num, input_nodes, target1, target1_state, target2, target2_state, attractors, state_key))
    db.commit()
    if i % 1000 == 0:
        print i
    assert(suc==1)
