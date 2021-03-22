#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

from autosklearn.regression import AutoSklearnRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
import numpy as np
import pandas as pd

from viz.pd_prof import get_us_df


def arr(a):
    """Input should be a 1-dimensional vector."""
    return np.array(a).reshape(-1, 1)  # This is a 2-D array, with single column.


def pnomial(x, a=0, b=0, c=4, d=5):
    return a * x**3 + b * x**2 + c * x + d


def get_curve(lo=0, hi=100, n_samples=1000, sigma=.5):
    df = pd.DataFrame(dict(x=np.linspace(lo, hi, n_samples)))
    df['y'] = df.x.apply(pnomial) + sigma * np.random.standard_normal(n_samples)

    df.x[0] = 950.
    df.y[0] = pnomial(df.x[0])
    df.x[1] = 980.
    df.y[1] = pnomial(df.x[1])
    return df


def main():
    df = get_us_df()
    print(len(df))
    # X = df.date
    # y = df.deaths

    df = get_curve()
    features = arr(df.x)
    target = arr(df.y)
    tscv = TimeSeriesSplit(n_splits=2)

    # xtrain, xtest, ytrain, ytest = train_test_split(features, target, test_size=0.2)
    for train_index, test_index in tscv.split(features):
        print("TRAIN:", len(train_index), "TEST:", len(test_index))
        assert max(train_index) < min(test_index)
        x_train, _ = features[train_index], features[test_index]
        y_train, _ = target[train_index], target[test_index]

    regressor = AutoSklearnRegressor(
        time_left_for_this_task=50,
        include_estimators=['ard_regression'])
    regressor.fit(x_train, y_train)
    print(regressor.show_models())
    print(regressor.sprint_statistics())

    df = get_curve(100, 900)
    pred = regressor.predict(arr(df.x))
    mae = mean_absolute_error(arr(df.y), pred)
    print("MAE:", mae)
    print(type(pred))
    df['pred'] = np.array(pred)
    df['delta'] = df.y - df.pred
    print(df)


if __name__ == '__main__':
    main()
