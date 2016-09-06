from pyhet import boolean2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#
# Using Piecewise linear differential equations
#
# This initial condition leads to damped oscillations
# If A is set to False, a steady state is obtained.
#
def test_this():

    text = """
    A = True    
    B = False
    C = False
    D = True

    1: B* = A or C
    1: C* = A and not D
    1: D* = B and C
    """
    model = boolean2.Model( text, mode='plde')
    model.initialize()
    model.iterate( fullt=7, steps=150 )
    
    # generate the plot
    #
    p1 = plt.plot( model.data["B"] , 'ob-' )
    p2 = plt.plot( model.data["C"] , 'sr-' )
    p3 = plt.plot( model.data["D"] , '^g-' )
    plt.legend( [p1,p2,p3], ["B","C","D"])
    plt.show()
    plt.savefig('t-06_output.jpg')

