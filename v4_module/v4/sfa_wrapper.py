import json

import networkx as nx
from networkx import json_graph
import pymysql

import sfap

def SFA_sim(dict_args):
    dict_args['perturbs'] = dict_args['perturb_targets']

    F, act, dg = sfap.analyze_signal_flow(dict_args)
    d_res = json_graph.node_link_data(dg)
    result = json.dumps(d_res)

    db = pymysql.connect(user='root', passwd='sbl4365', db='v4', charset='utf8')
    cursor = db.cursor()

    sql = "UPDATE ANALYSIS_RESULT SET SFA_NETWORK_JSON=%s WHERE ANALYSIS_ID=%s and TREATMENT_ID=%s"
    cursor.execute(sql, (result, int(dict_args['patient_id']), int(dict_args['treatment_id'])))
    db.commit()
    db.close()
