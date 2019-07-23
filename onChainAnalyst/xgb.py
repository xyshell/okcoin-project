
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from util import *

import xgboost as xgb
import operator
from sklearn.model_selection import train_test_split


def split_data(data, training_size=0.8):
    """
    data: Pandas Dataframe
    training_size: proportion of the data to be used for training
    Return: train_set and test_set as pandas DataFrame
    """
    return data[:int(training_size*len(data))], data[int(training_size*len(data)):]


def feature_importance_plot(importance_sorted, title):
    df = pd.DataFrame(importance_sorted, columns=['feature', 'fscore'])
    df['fscore'] = df['fscore'] / df['fscore'].sum()

    plt.figure()
    # df.plot()
    df.plot(kind='barh', x='feature', y='fscore', legend=False, figsize=(12, 10))
    plt.title('XGBoost Feature Importance')
    plt.xlabel('relative importance')
    plt.tight_layout()
    plt.savefig(title + '.png', dpi=300)
    plt.show()


def xgb_importance(df, test_ratio, xgb_params, ntree, early_stop, plot_title):
    df = pd.DataFrame(df)
    # split the data into train/test set
    X = df.iloc[:, 0:5]
    Y = df.iloc[:, 5]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_ratio, random_state=42)

    dtrain = xgb.DMatrix(X_train, y_train)
    dtest = xgb.DMatrix(X_test, y_test)

    watchlist = [(dtrain, 'train'), (dtest, 'validate')]

    xgb_model = xgb.train(xgb_params, dtrain, ntree, evals=watchlist, early_stopping_rounds=early_stop, verbose_eval=True)

    importance = xgb_model.get_fscore()
    importance_sorted = sorted(importance.items(), key=operator.itemgetter(1))
    feature_importance_plot(importance_sorted, plot_title)


def xgb_result_compare(y_val, y_pred):
    '''
    :param y_val: pandas Series, actually price of Tether
    :param y_pred: pandas Series, predicted price of Tether
    Picture actual VS. predicted result
    '''
    n = len(y_val)
    x = np.arange(0, n, 1)
    
    plt.plot(x, y_val, color="r", linestyle="-", marker="^", linewidth=1)
    plt.plot(x, y_pred, color="b", linestyle="-", marker="s", linewidth=1)
    
    plt.xlabel("numbers")
    plt.ylabel("actual VS. predicted")

    plt.show()
