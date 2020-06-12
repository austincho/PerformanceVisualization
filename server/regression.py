import csv

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from server.app import *

def predict(input, prediction):
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

    print(X_train_imp_encode.shape)
    print("===========")
    print(y_train.shape)

    lr = Ridge()
    lr.fit(X_train_imp_encode, y_train)

    predictions = []

    # now predict can be used with lr
    for x in range(input + 1, prediction + 1):
        predictions.extend(lr.predict([[x]]))

    return {"predictions": predictions,
            "actual": actual}
