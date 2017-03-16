import cPickle as pickle
import numpy as np
from kmodes import kmodes

f = open('total_atts.p','rb')
a = pickle.load(f)
f.close()
total_atts = a['total_atts']
total_atts_state_key = a['total_atts_state_key']

inputs = np.zeros([len(total_atts),96])

for i in range(len(total_atts)):
    inputs[i] = np.fromstring(total_atts[i],'u1').reshape([1,-1]) - ord('0')

km = kmodes.KModes(n_clusters=3, init='Huang', n_init=5, verbose=1)

clusters = km.fit_predict(inputs)

outputs = {'cluster':clusters, 'total_atts':total_atts, 'total_atts_state_key':total_atts_state_key}
f = open('att_cluster.p','wb')
pickle.dump(outputs,f)
f.close()
