#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

from autosklearn.regression import AutoSklearnRegressor
from sklearn.datasets import load_boston
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import pandas as pd

from viz.pd_prof import get_us_df


def main():
    df = get_us_df()
    print(len(df))
    # X = df.date
    # y = df.deaths

    boston_data = load_boston()
    features = pd.DataFrame(boston_data.data, columns=boston_data.feature_names)
    target = pd.DataFrame(boston_data.target, columns=['TARGET'])
    # dataset = pd.concat([features, target], axis=1)
    xtrain, xtest, ytrain, ytest = train_test_split(features, target, test_size=0.2)

    regressor = AutoSklearnRegressor(time_left_for_this_task=60)
    regressor.fit(xtrain, ytrain)
    print(regressor.sprint_statistics())
    print(regressor.show_models())

    pred = regressor.predict(xtest)
    mae = mean_absolute_error(ytest, pred)
    print("MAE:", mae)


if __name__ == '__main__':
    main()
