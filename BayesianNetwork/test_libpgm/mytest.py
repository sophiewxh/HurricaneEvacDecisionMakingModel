import pandas as pd
import numpy as np
import json
from libpgm.graphskeleton import GraphSkeleton
from libpgm.pgmlearner import PGMLearner
from pprint import pprint
import os


def select_vars(df):

    for i, row in df.iterrows():       
        # can also use np.where
        if row['coast_dist'] < 2.0:
            df.set_value(i, 'close_to_coast', 1)
        else:
            df.set_value(i, 'close_to_coast', 0)
            
        if row['issued_mandatory']==1 or row['issued_voluntary']==1:
            df.set_value(i, 'issued_order', 1)
        else:
            df.set_value(i, 'issued_order', 0)
    

    obj_cols = ['issued_order','close_to_coast','ht_mobile', 
                'income_above_4k', 'pets', 'have_child',
                'evac']
    
    for col in obj_cols:
        df[col] = df[col].astype(float)
        
    df1 = df[obj_cols]
    return df1
    #df1.to_csv("Ivan_common_test4.csv", index=False)
    
def test_libpgm(df1):

    data = df1.T.to_dict().values()
    #pprint(data)
    skel = GraphSkeleton()
    skel.load("bn_struct.txt")
    
    learner = PGMLearner()
    result = learner.discrete_mle_estimateparams(skel, data)
    
    print json.dumps(result.Vdata, indent=2)
    
if __name__ == '__main__':
    fp = 'C:\Users\Sophie\workspace\Hurricane\BayesianNetwork\data\Ivan_common.csv'
    df = pd.read_csv(fp)
    df1 = select_vars(df)
    test_libpgm(df1)
    #print os.getcwd()
