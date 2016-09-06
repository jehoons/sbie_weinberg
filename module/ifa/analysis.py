import hashlib
import boolean2
import pandas as pd
import json
from ipdb import set_trace
from boolean2 import Model
from util import update_progress

def find_attractors(model=None, steps=10, mode='sync', sample_size=1000):

    simulation_data = { }
    seen = {}
    fingerprint_mapping = {}

    for i in range(sample_size):
        update_progress(i, sample_size)

        model.initialize()
        model.iterate( steps=steps )
        index,size = model.detect_cycles()
        key = model.first.fp()

        values = [ x.fp() for x in model.states[:steps] ]

        if size == 1:
            attr_type = 'point'

        elif size > 1:
            attr_type = 'cyclic'

        elif size == 0:
            attr_type = 'unknown'

        if attr_type == 'cyclic':
            cyc_traj = values[index:index + size]
            cyc_hash = hashlib.sha224(repr(sorted(cyc_traj))).hexdigest()
            cyc_hash = cyc_hash[0:20]
            attr_id = cyc_hash 
            
        else: 
        	attr_id = values[-1]

        seen [str(key)] = {
            'index':index, 
            'size':size,
            'trajectory': values,
            'type': attr_type,
            'initial': values[0],
            'attractor': attr_id
            }

        for x in model.states:
            fingerprint_mapping[ str(x.fp()) ] = x.values()

    simulation_data = {
        'fingerprint_map': fingerprint_mapping,
        'fingerprint_map_keys': x.keys(),
        'attractors': seen
        }

    df = pd.DataFrame([], columns=[
        'initial_state','attractor', 'cyclic_attractor'])
    
    cyclic_attr_info = {}
    j = 0
    for initial in simulation_data['attractors'].keys():
        if simulation_data['attractors'][str(initial)]['type'] == 'unknown':
            continue

        attr = simulation_data['attractors'][str(initial)]['attractor']
        attr_type = simulation_data['attractors'][str(initial)]['type']
        df.loc[j, 'initial_state'] = str(initial)
        df.loc[j, 'type'] = attr_type

        if attr_type == 'point':
            df.loc[j, 'attractor'] = attr

        elif attr_type == 'cyclic':
            traj = simulation_data['attractors'][str(initial)]['trajectory']
            idx = simulation_data['attractors'][str(initial)]['index']
            sz = simulation_data['attractors'][str(initial)]['size']
            cyc_traj = traj[idx:idx+sz]
            cyc_hash = hashlib.sha224(repr(sorted(cyc_traj))).hexdigest()
            cyc_hash = cyc_hash[0:20]
            df.loc[j, 'attractor'] = cyc_hash
            cyclic_attr_info[cyc_hash] = cyc_traj

        j += 1

    simulation_data['cyclic_attractor_info'] = cyclic_attr_info

    basin = df.groupby('attractor')['initial_state'].count().to_frame()
    basin.rename(columns={'initial_state': 'basin_size'}, inplace=True)
    basin = basin.to_dict()['basin_size']

    for old_key in basin.keys():
        new_key = str(old_key)
        basin[new_key] = int( basin.pop(old_key) )

    simulation_data['basin_of_attraction'] = basin

    attr_type_data = {}
    for i in df.index:
        attr =  df.loc[i, 'attractor']
        attr_type = df.loc[i, 'type']
        attr_type_data[attr] = attr_type

    simulation_data['attractor_info'] = attr_type_data

    return simulation_data


def test_find_attractors():

    from pyhet.boolean2 import Model
    from pyhet.analysis import find_attractors

    # text = """
    # A = Random
    # B = Random
    # C = Random
    # D = Random
    #
    # A *= D or C
    # B *= A
    # C *= B or D
    # D *= B
    # """

    # Random sampling of initial conditions
    #
    # If A is set to False, a steady state is obtained.
    #
    #
    # text = """
    # A = True
    # B = Random
    # C = Random
    # D = Random
    #
    # B* = A or C
    # C* = A and not D
    # D* = B and C
    # """

    text = """
    A = True
    B = Random
    C = Random
    D = Random

    B* = A or C
    C* = A and not D
    D* = B and C
    """

    model = Model( text=text, mode='sync')
    res = find_attractors(model=model, steps=100, sample_size=100000)

    outputfile = 'output.json'
    json.dump(res, open(outputfile, 'w'), indent=1)


