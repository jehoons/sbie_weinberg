import json
from information_processing_network.boolean2 import Model
from information_processing_network.analysis import find_attractors
from ipdb import set_trace

def test_compute_basin():

    text = """
    A = Random
    B = Random
    C = Random
    D = Random

    A *= D or C
    B *= A
    C *= B or D
    D *= B
    """

    model = Model( text=text, mode='sync')
    res = find_attractors(model=model, sample_size=10000)
    print (res)

    outputfile = 'output.json'
    json.dump(res, open(outputfile, 'w'), indent=1)

    # set_trace()
