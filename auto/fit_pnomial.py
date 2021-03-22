#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def arr(a):
    """Input should be a 1-dimensional vector."""
    return np.array(a).reshape(-1, 1)  # This is a 2-D array, with single column.


def pnomial(x, a=0, b=3, c=4, d=5):
    return a * x**3 + b * x**2 + c * x + d


def get_curve(lo=0, hi=100, n_samples=1000, sigma=2e3):
    df = pd.DataFrame(dict(x=np.linspace(lo, hi, n_samples)))
    df['y'] = df.x.apply(pnomial) + sigma * np.random.standard_normal(n_samples)
    return df


def main():
    df = get_curve()
    poly_features = PolynomialFeatures(degree=2, include_bias=False)
    x_poly = poly_features.fit_transform(arr(df.x))
    lin_reg = LinearRegression()
    lin_reg.fit(x_poly, df.y)
    print(lin_reg.intercept_, lin_reg.coef_)

    df = get_curve(-300, 500)
    x = arr(df.x)
    x = poly_features.transform(x)

    pred = lin_reg.predict(x)
    mae = mean_absolute_error(arr(df.y), pred)
    print("MAE:", mae)
    print(type(pred))
    df['pred'] = np.array(pred)
    df['delta'] = df.y - df.pred
    print(df)

    fig, ax = plt.subplots()
    ax.plot(df.x, df.y, label='signal')
    ax.plot(df.x, pred, label='predicted')
    ax.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    main()