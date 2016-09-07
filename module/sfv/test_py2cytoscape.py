# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 10:30:20 2016

@author: dwlee
"""
import pandas as pd
import json

from py2cytoscape.data.cynetwork import CyNetwork
from py2cytoscape.data.cyrest_client import CyRestClient

from sysbio.util import read_sif
from sysbio.util import convert_networkx_digraph


A, name_to_idx = read_sif("fumia_network.sif")
dg = convert_networkx_digraph(A, name_to_idx)

cy = CyRestClient()

#cy.session.delete()
network1 = cy.network.create_from_networkx(dg)

# Visual Properties (VPS)
vps = pd.Series(cy.style.vps.get_all())
vps.head(20)


# Get views for a network: Cytoscape "may" have multiple views, and that's why it returns list instead of an object.
view_id_list = network1.get_views() 

# Display IDs of available views
print(view_id_list)

# The "format" option specify the return type.
view1 = network1.get_view(view_id_list[0], format='view')

# This is a CyNetworkView object, not dictionary
print(view1)

# As a json format
view2 = network1.get_view(view_id_list[0], format='json')

# Get node/edge views as a Python dictionary
node_views_dict = view1.get_node_views_as_dict() 
edge_views_dict = view1.get_edge_views_as_dict() 

# Convert it into Pandas DataFrame
nv_df = pd.DataFrame.from_dict(node_views_dict, orient='index' )

# Extract specific Visual Property values...
node_location_df = nv_df[['NODE_X_LOCATION', 'NODE_Y_LOCATION']]
node_location_df.head()



###############################################################################
# Set random colors to nodes

# Switch current visual stye to a simple one...
minimal_style = cy.style.create('Minimal')
cy.style.apply(style=minimal_style, network=network1)
cy.layout.apply(name='force-directed', network=network1)

# Change background color:  simply pass key-value pair
view1.update_network_view(visual_property='NETWORK_BACKGROUND_PAINT',
                          value='white')

# Get SUID of all nodes
target_nodes = network1.get_nodes()

# Generate random colors for each node
import random

def get_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return '#' + hex(r)[2:] + hex(g)[2:] + hex(b)[2:]

# Assign key-value pair.  For this example, node SUID to color.
def generate_randome_color_dict(node_ids):
    new_values = {}
    for n in node_ids:
        new_values[n] = get_color()
    return new_values

new_values = generate_randome_color_dict(target_nodes)

# Set new values for a set of nodes.  In this case, all nodes in the network
view1.update_node_views(visual_property='NODE_FILL_COLOR',
                        values=new_values)
                        
                        
        