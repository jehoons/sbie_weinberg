import numpy as np
import json

def test_makerandinp():

    config = {
            'id': 0, 
            's1coef': 'min', 
            's1reff': False, 
            's1alp': 1.0, 
            's2coef': 'min', 
            's2reff': True, 
            's2alp': 1.0, 
            'working_root': './datafiles'
            }

    for i in range(1, 1000 + 1): 
        print i,
        config['id'] = i
        config['s1coef'] = ['min', '1se'][np.random.randint(2)]
        config['s1reff'] = [True, False][np.random.randint(2)]
        config['s1alp'] = 0.8 + np.random.uniform()*0.2
        config['s2coef'] = ['min', '1se'][np.random.randint(2)] 
        config['s2reff'] = [True, False][np.random.randint(2)] 
        config['s2alp'] = 0.8 + np.random.uniform()*0.2

        conffile = 'input%04d.json' % i 

        json.dump(config, open(conffile,'wb'), separators=(',',':'), 
                sort_keys=True, indent=2) 


