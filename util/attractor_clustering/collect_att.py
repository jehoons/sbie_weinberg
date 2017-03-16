import json
import numpy as np
import cPickle as pickle

def hamming(s1, s2):
    assert(len(s1) == len(s2))
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

f = open('/data/Table-S7H-Scanning-results-APC.json','r')
result = json.load(f)
f.close()
result = result["scanning_results"]

total_record = len(result)

total_atts = np.array([])
total_atts_state_key = np.array([])

tatemp = np.array([])
tasktemp = np.array([])
for i in range(len(result)):
    temp = result[i]
    attnum = len(temp['attractors'])
    attkeys = temp['attractors'].keys()
    for j in range(attnum):
        atttemp = temp['attractors'][attkeys[j]]
        if atttemp['type'] == 'unknown':
            continue
        elif atttemp['type'] == 'point':
            tasktemp = np.append(tasktemp, atttemp['value'])
            tatemp = np.append(tatemp, temp['state_key'][atttemp['value']])
        else: #cyclic
            cyc = atttemp['value']
            for k in cyc:
                tasktemp = np.append(tasktemp, k)
                tatemp = np.append(tatemp, temp['state_key'][k])
    if i%1000 == 0:
        print i
        total_atts = np.append(total_atts, tatemp)
        total_atts_state_key = np.append(total_atts_state_key, tasktemp)
        tatemp = np.array([])
        tasktemp = np.array([])

total_atts = np.append(total_atts, tatemp)
total_atts_state_key = np.append(total_atts_state_key, tasktemp)

_, indices = np.unique(total_atts_state_key, return_index=True)
total_atts = total_atts[indices]
total_atts_state_key = total_atts_state_key[indices]

f = open('total_atts.p','wb')
temp = {'total_atts':total_atts, 'total_atts_state_key':total_atts_state_key}
pickle.dump(temp,f)
f.close()

#hamdist = np.zeros([len(indices)*(len(indices)-1)/2])
#k = 0
#for i in range(len(total_atts)-1):
#    for j in range(i+1,len(total_atts)):
#        hamming_matrix[k] = hamming(total_atts_state_key[i], total_atts_state_key[j])
#        k = k + 1

#f = open('hamming_dist.p','wb')
#pickle.dump(hamming_matrix,f)
#f.close()
