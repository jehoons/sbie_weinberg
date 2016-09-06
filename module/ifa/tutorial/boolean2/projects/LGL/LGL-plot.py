"""
Plots results for the paper

"""
from matplotlib import pyplot as plt 
# from pylab import *
from pyhet.boolean2 import util

def smooth(data, w=0):
    "Smooths data by a moving window of width 'w'"
    fw = float(w)
    def average( index ):
        return sum( data[index: index+w] )/fw
    indices = xrange( len(data) - w )        
    out = map( average, indices )
    return out

def make_plot():
    
    # contains averaged node information based on 1000 runs
    data = util.bload( 'LGL-run.bin' )

    # each of these is a dictionary keyed by nodes
    run1, run2, run3, run4 = data 

    # applies smoothing to all values
    for run in (run1, run2, run3, run4):
        for key, values in run.items():
            run[key] = smooth( values, w=10 )
    
    #
    # Plotting Apoptosis
    #
    plt.subplot(121)
    apop1, apop2, apop3, apop4 = 
        run1['Apoptosis'], 
        run2['Apoptosis'],
        run3['Apoptosis'],
        run4['Apoptosis']

    ps1, = plt.plot( apop1, 'bo-')
    ps2, = plt.plot( apop2, 'ro-')
    ps3, = plt.plot(apop3,'b^-') 
    ps4, = plt.plot(apop4,'r^-')

    plt.legend( [ps1,ps2,ps3,ps4], 
        ['Normal-Apop', 'MCL1-over-Apop','sFas-over-Apop','LGL-like-Apop' ],
        loc='best')

    plt.title('Changes in Apoptosis')
    plt.xlabel( 'Time Steps' )
    plt.ylabel( 'Percent (%)' )
    plt.ylim( (-0.1, 1.1) )

    #
    # Plotting FasL and Ras
    #
    plt.subplot(122)
    fasL1, fasL2 = run1['FasL'], run4['FasL']
    ras1, ras2 = run1['Ras'], run4['Ras']

    ps1, = plt.plot( fasL1, 'bo-' )
    ps2, = plt.plot( fasL2, 'ro-' )
    ps3, = plt.plot( ras1, 'b^-' )
    ps4, = plt.plot( ras2, 'r^-' )
    
    plt.legend([ps1, ps2, ps3, ps4],
        'Normal-FasL LGL-like-FasL Normal-Ras LGL-like-Ras'.split(),
        loc='lower left' )

    plt.title( ' Changes in FasL and Ras' )
    plt.xlabel( 'Time Steps' )

# if __name__ == '__main__':
def test_main():
    # resize this to change figure size
    plt.figure(num = None, figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
    make_plot( )
    plt.savefig('Figure2.png')
    plt.show()


