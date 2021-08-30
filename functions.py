"""
preprocessing function
"""


#%% import libraries

import numpy as np
import pandas as pd 



#%%


def array_to_df(lst):
    numpy_array = np.array(lst)
    df = pd.DataFrame([numpy_array],columns=["bedrooms","bathrooms","sqft_living","sqft_lot","floors","waterfront","view","condition","sqft_above","sqft_basement","yr_built","yr_renovated","city","statezip","country"])
    return df 



def testpre_processing(df0):
    df = df0.copy()
    columns_drop = ["date","street"]
    for column in df.columns:
        if column in columns_drop:
            df = df.drop(column,axis=1)
    column_dummies =["statezip","country","city"]
    for column in df.columns:
        if column in column_dummies:
             df_dummies = pd.get_dummies(df[column],prefix=column)
             df= pd.concat([df,df_dummies],axis=1)
             df = df.drop(column,axis=1)
    df_zero = pd.DataFrame(np.zeros((1,119)))
    df = pd.concat([df,df_zero],axis=1)
    return df

#%%