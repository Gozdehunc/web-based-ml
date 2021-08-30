"""
House Price Prediction

"""
#%% import libraries

import os
import numpy as np
from numpy.lib.arraysetops import unique
from numpy.lib.function_base import append
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.sparse import data
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import pickle




#%% load data 

if os.path.isdir("/kaggle/input"):
    file_name_train = "/kaggle/input/housedata/data.csv"
    
    
else:
    file_name_train = "data.csv"
   
    
df = pd.read_csv(file_name_train)
#%% plot corr graph

corr1 = df.corr()
corr1 = corr1.T

#%% categorical columns values 
# total number of rows : 4600
street = df["street"].value_counts()       #4525 different values  street column definitely should be drop.
city = df["city"].value_counts()           #44 different values    get_dummies
state_zip = df["statezip"].value_counts()  #77 different values    get_dummies
country = df["country"].value_counts()     #1 different values     get_dummies
#%% statezip ve city arasındaki bağlantıyı bul.
#sns.scatterplot(x="city",y="statezip",data=df)
#plt.show()

city_value = df["city"].unique()

#%% none value counts 
none_values = df.isna().sum()  #There are not None,null values in this dataset.
#%% zeros values counts 
zeros_values =(df==0).sum() #There are zero values in this dataset.
print(zeros_values)
# price              49    # The highest associated column by the correlation is sqft_living. So we fill zero
                           #price values according to sqft_living column's median.
# bedrooms            2   two houses have no bedrooms.!
# bathrooms           2   two houses have no bathrooms.!
# waterfront       4567   maybe can
# view             4140   maybe can
# sqft_basement    2745   we filled sqft_basement column zero values according to the highest
                          # correlation associated column median value

# yr_renovated     2735 
#%%
describe = df.describe()
#%% plot condition
sns.barplot(x="condition",y="price",data=df)
plt.show()

number_of_condition =df["condition"].value_counts()

#%% plot (bedrooms)

sns.barplot(x="bedrooms",y="price",data=df)
plt.show()

#%% plot (bathrooms)

sns.barplot(x="bathrooms",y="price",data=df)
plt.show()
number_of_bedrooms = df["bedrooms"].value_counts()
#%%

sns.scatterplot(x="sqft_basement",y="price",data=df)
plt.show()

#%%

sns.scatterplot(x="yr_renovated",y="price",data=df)
plt.show()

#%%
yr_renovated = df["yr_renovated"].value_counts()
yr_renovated_copy = df[(df["yr_renovated"]>0)].copy()
median_yr = yr_renovated_copy["yr_renovated"].mean()


bedrooms_values =df["bedrooms"].value_counts()
bathrooms_values = df["bathrooms"].value_counts()
#%%
def fill_zero(cols):

    price = cols[0]
    sqft_above = cols[1]
    if price ==0:
        return int(df[df["sqft_above"]==sqft_above]["price"].median())
    else:
        return price


df["price"] = df[["price","sqft_above"]].apply(fill_zero,axis=1)
#%% statezip

city_statezip = df.groupby("city")["statezip"].count().sort_values(ascending=False).to_frame()
# how many different zip codes are there in each city?
city_statezip_unique = df.groupby("city")["statezip"].nunique().reset_index()

city_price = df.groupby("city")["price"].median().sort_values(ascending=False)
statezip_price = df.groupby("statezip")["price"].max().sort_values(ascending=False)
#%%
df_real = df[(df["yr_built"]>df["yr_renovated"]) & (df["yr_renovated"]!=0)]
df = df.drop(df_real.index,axis=0)
#%% remove zero bedrooms and bathrooms

df["bedrooms"] = df["bedrooms"].replace(0,7)
df["bedrooms"] = df["bedrooms"].replace(9,3)
df["bathrooms"] = df["bathrooms"].replace(0,3.25)
df["sqft_basement"] = df["sqft_basement"].replace(0,df["sqft_living"].median())


def year_renovated(cols):
    renovated=cols[0]
    built =cols[1]
    if built>1994:
        None
    elif renovated==0 and built<1994:
        renovated =1994
    return renovated
df["yr_renovated"] = df[["yr_renovated","yr_built"]].apply(year_renovated,axis=1)



#%% conditionlara göre price ortalamalarına bak.
# Calculate the house price mean according to contidion value.
condition = df["condition"].value_counts().to_frame().reset_index() # we create a DataFrame about condition
condition_unique =df["condition"].unique()

def calc_condit(cols):
    index =cols[0]
    return int(df[df["condition"]==index]["price"].mean())

condition["cond_price"] =condition[["index"]].apply(calc_condit,axis=1)
#%% df copy ile devam ettik.

df_copy = df[(df["price"]<1500000)].copy()
df_copy1 = df_copy[(df_copy["city"]=="Seattle") & (df_copy["price"]<600000) & (df_copy["condition"]==4)]
df_copy=df_copy.drop(df_copy1.index,axis=0)

#%%

def pre_processing(df0):
    df = df0.copy()
    columns_drop = ["date","street"]
    for column in df.columns:
        if column in columns_drop:
            df = df.drop(column,axis=1)
    column_dummies =["statezip","city","country"]
    for column in column_dummies:
        df_dummies = pd.get_dummies(df[column],prefix=column)
        df= pd.concat([df,df_dummies],axis=1)
        df = df.drop(column,axis=1)
    
    return df

#%% preprocessing(for train)

df_copy = pre_processing(df_copy)

#%%
def train_split(df0):
    df=df0.copy()
    y= df["price"]
    x = df.drop("price",axis=1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3,random_state=18
                                                    )
    return x_train,x_test,y_train,y_test

x_train, x_test,y_train ,y_test = train_split(df_copy)

def fit(x_train, y_train, x_test,y_test):
    regressor = GradientBoostingRegressor(n_estimators=500, random_state=23)
    regressor.fit(x_train, y_train)
    score = regressor.score(x_test, y_test)
    print(score)    #0.7784
    #predictions = model.predict(df_test)
    pickle.dump(regressor, open('model.pkl','wb'))


fit(x_train, y_train, x_test,y_test)

#%%last
df.info()










# %%
