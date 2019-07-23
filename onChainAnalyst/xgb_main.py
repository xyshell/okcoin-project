
# Import libraries
import numpy as np
import pandas as pd
from util import *
from xgb import *
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from xgboost.sklearn import XGBRegressor  # wrapper
import scipy.stats as st

# Import dataset
dataset = pd.read_csv('data/dataset.csv')
start_time = '2019-07-17 00:00:00'
timestamp = str_to_tstp(start_time)
dataset = dataset[dataset['time']>timestamp]

# Modify importing feature
time_1 = dataset['time'].shift(1)
time_interval = dataset['time']-time_1

training_data = pd.DataFrame()
training_data['time_interval'] = time_interval
training_data['former_price'] = dataset['price'].shift(1)
training_data['amount'] = dataset['amount']
training_data['exchange_type'] = dataset['exchange_type']
training_data['transaction_times'] = dataset['transaction_times']
training_data['price'] = dataset['price']
training_data = training_data.iloc[1:, :]


# Divide data into input data X and output data y
X = training_data.iloc[:, 0:5].values
y = training_data.iloc[:, 5].values


# ===================See what input feature have higher weight=====================

# base parameters
xgb_params = {
    'booster': 'gbtree',
    'objective': 'reg:linear',  # regression task
    'subsample': 0.80,  # 80% of data to grow trees and prevent overfitting
    'colsample_bytree': 0.85,  # 85% of features used
    'eta': 0.1,
    'max_depth': 10,
    'seed': 42}  # for reproducible results

val_ratio = 0.3
ntree = 300
early_stop = 50

print('-----Xgboost Using All Numeric Features-----', 
      '\n---inital model feature importance---')
fig_allFeatures = xgb_importance(training_data, val_ratio, xgb_params, ntree, 
                                 early_stop, 'All Features')
plt.show()

# ===================Train Model there to find best parameters=====================
print('\n-----Xgboost on only datetime information---------\n')
dim = {'train and validation data ': training_data.shape}
print(pd.DataFrame(list(dim.items()), columns=['Data', 'dimension']))

# train model
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=val_ratio, random_state=42)

dtrain = xgb.DMatrix(X_train, y_train)
dval = xgb.DMatrix(X_val, y_val)
watchlist = [(dtrain, 'train'), (dval, 'validate')]

# Grid Search
params_sk = {'objective': 'reg:linear',
             'subsample': 0.8,
             'colsample_bytree': 0.85,
             'seed': 42}

skrg = XGBRegressor(**params_sk)

skrg.fit(X_train, y_train)

params_grid = {"n_estimators": st.randint(100, 500),
               # "colsample_bytree": st.beta(10, 1),
               # "subsample": st.beta(10, 1),
               # "gamma": st.uniform(0, 10),
               # 'reg_alpha': st.expon(0, 50),
               # "min_child_weight": st.expon(0, 50),
               # "learning_rate": st.uniform(0.06, 0.12),
               'max_depth': st.randint(6, 30)
               }
search_sk = RandomizedSearchCV(skrg, params_grid, cv=5, random_state=1, n_iter=20)

# 5 fold cross validation
search_sk.fit(X, y)

# best parameters
print("best parameters:", search_sk.best_params_)
print("best score:", search_sk.best_score_)

# with new parameters
params_new = {**params_sk, **search_sk.best_params_}

nrg = XGBRegressor(**params_new)
nrg.fit(X_train, y_train)

# Predicted y with best parameters
y_pred = nrg.predict(X_val)

# Show result in picture
xgb_result_compare(y_val, y_pred)
