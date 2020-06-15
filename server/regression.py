import csv

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from scipy.optimize import curve_fit

from app import *


def fib_exp_regression(predict_vals):
    def exponential(x, a, b):
        return a * np.exp(b * x)

    y = pd.read_csv("./final.csv", header=0, index_col=False)["tottime"].tolist()
    X = np.arange(len(y))
    pars, _ = curve_fit(f=exponential, xdata=list(range(1, len(y) + 1)), ydata=y, p0=[0, 0],
                        bounds=(-np.inf, np.inf))

    # curve = exponential(X, *pars)

    x_project = np.arange(predict_vals)
    predictions = exponential(np.array(x_project), *pars)

    return {
        "actual": y,
        "predictions": predictions[len(y):].tolist()
    }


def merge_sort_poly_regression(predict_vals):
    def nlogn(X):
        val = np.log(X)
        val[val == -np.inf] = 0
        return np.multiply(val, X)

    y = pd.read_csv('./final.csv')['tottime'].tolist()
    X = np.arange(len(y))
    coefficients = np.polyfit(nlogn(X), y, 1)
    fit = np.poly1d(coefficients)

    x_predict = np.arange(predict_vals)

    return {
        'actual': y,
        'predictions': fit(nlogn(x_predict))[len(X):].tolist()
    }


def linear_regression(predict_vals):
    y = pd.read_csv('./final.csv')['tottime'].tolist()
    X = np.arange(len(y))
    lr = Ridge()
    lr.fit(X.reshape(-1, 1), y)

    x_predict = np.arange(len(y), predict_vals)
    predictions = lr.predict(x_predict.reshape(-1, 1))

    return {
        'actual': y,
        'predictions': predictions.tolist()
    }

def predict(fn_code, inputVal, predictionVal):
    if fn_code == 1:
        return fib_exp_regression(predictionVal)
    elif fn_code == 3:
        return merge_sort_poly_regression(predictionVal)
    else:
        return linear_regression(predictionVal)
    actual = []
    df_train = pd.read_csv("./final.csv", header=0, index_col=False)
    actual = df_train["tottime"].tolist()
    df_train, df_test = train_test_split(df_train, test_size=0.1, random_state=100)

    target = ["tottime"]
    numeric_features = ["ncalls"]
    all_features = numeric_features

    imputers = [
        ("numeric", SimpleImputer(strategy="median"), numeric_features)
    ]

    impute_transformer = ColumnTransformer(transformers=imputers)
    impute_transformer.fit(df_train)

    df_train_imp = pd.DataFrame(impute_transformer.transform(df_train), index=df_train.index, columns=all_features)
    df_test_imp = pd.DataFrame(impute_transformer.transform(df_test), index=df_test.index, columns=all_features)

    feature_transformers = [
        ('scale', StandardScaler(), numeric_features)
    ]

    feature_preprocessor = ColumnTransformer(transformers=feature_transformers)
    feature_preprocessor.fit(df_train_imp)

    X_train_imp_encode = feature_preprocessor.transform(df_train_imp)
    X_test_imp_encode = feature_preprocessor.transform(df_test_imp)

    df_train_imp_encode = pd.DataFrame(X_train_imp_encode, index=df_train_imp.index, columns=numeric_features)
    df_test_imp_encode = pd.DataFrame(X_test_imp_encode, index=df_test_imp.index, columns=numeric_features)

    y_train = df_train["tottime"]
    y_test = df_test["tottime"]

    # print(X_train_imp_encode.shape)
    # print("===========")
    # print(y_train.shape)

    lr = LinearRegression()
    lr.fit(X_train_imp_encode, y_train)

    predictions = []

    # now predict can be used with lr
    for x in range(inputVal + 1, predictionVal + 1):
        predictions.extend(lr.predict([[x]]))

    return {"predictions": predictions,
            "actual": actual}
