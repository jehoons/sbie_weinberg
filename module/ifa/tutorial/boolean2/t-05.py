# The collector helper function
#
# Asynchronous updating rules are non deterministic and
# need to be averaged over many runs
#
# The collector class makes this averaging very easy. It takes
# a list of states and nodes to build a data structure that 
# can compute the average the state of each node over all simulation and each timestep.
#
# The output of averaging (in the normalized mode) is a value between
# 0 and 1 representing the fraction of simulation (multiply by 100 to get percent) 
# that had the node in state True. 
#
from pyhet import boolean2
from pyhet.boolean2 import util
from matplotlib import pyplot as plt
from pyhet.util import update_progress

def test_main():
    text = """
    A = True
    B = Random
    C = Random
    D = Random

    B* = A or C
    C* = A and not D
    D* = B and C
    """

    repeat = 5000

    coll  = util.Collector()
    for i in range(repeat):
        update_progress(i, repeat)
        model = boolean2.Model( text, mode='async')
        model.initialize()
        model.iterate( steps=15 )         
        # in this case we take all nodes
        # one could just list a few nodes such as [ 'A', 'B', 'C' ]
        nodes = model.nodes
        # this collects states for each run
        coll.collect(states=model.states, nodes=nodes)

    # this step averages the values for each node
    # returns a dictionary keyed by nodes and a list of values
    # with the average state for in each timestep
    avgs = coll.get_averages( normalize=True )

    # make some shortcut to data to for easier plotting
    valueB = avgs["B"]
    valueC = avgs["C"]
    valueD = avgs["D"]

    #
    # plot the state of the nodes
    #
    p1, = plt.plot( valueB , 'ob-' )
    p2, = plt.plot( valueC , 'sr-' )
    p3, = plt.plot( valueD , '^g-' )
    plt.legend( [p1,p2,p3], ["B","C","D"])

    plt.show()

    plt.savefig('t-05_figure.png')

