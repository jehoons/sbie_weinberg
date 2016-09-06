import os
from pdb import set_trace
import matplotlib

def test_hist2d_plot():
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.random.randn(1000)
    y = np.random.randn(1000) + 5
    # normal distribution center at x=0 and y=5
    plt.hist2d(x, y, bins=40)
    plt.show()



