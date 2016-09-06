import networkx as nx 
from pdb import set_trace 
import matplotlib.pyplot as plt

def test_main():
    G = nx.read_gml('timemodel.gml')
    nx.write_gml(G,"timemodel_2.gml")
    # print G.node
    nx.draw(G)
    plt.savefig('output.png')
    