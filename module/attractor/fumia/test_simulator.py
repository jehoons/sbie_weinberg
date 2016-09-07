import pytest
import os
from os.path import join,dirname,abspath,basename,exists

from sbie_weinberg.module.attractor.fumia import simulator as attr_simulator
from sbie_weinberg.dataset import demo
import glob

if not exists(join(dirname(__file__), 'untracked')):
    os.mkdir(join(dirname(__file__), 'untracked'))


def test_single_inputjson():

    infile = join(attr_simulator.matlab_root, 'test_input.json')
    # outputjson = join(attr_simulator.matlab_root, 'test_output.json')

    outputjson = join(abspath(dirname(__file__)), 'untracked', \
        'out_single_input.json')

    attr_simulator.run(infile, outputjson, time_length=10, sample_size=5)


# @pytest.mark.skipif(True, reason='no reason')
def test_many_inputjson():

    files = glob.glob(join(dirname(demo.__file__), 'demoinput*.json'))
    for inputjson in files:
        outputjson = join(abspath(dirname(__file__)), 'untracked', \
            'out_' + basename(inputjson))

        attr_simulator.run(inputjson, outputjson, time_length=10, sample_size=5)


