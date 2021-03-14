#! /usr/bin/env streamlit run

import numpy as np
import pandas as pd
# import statsmodels.api as sm
import statsmodels.formula.api as smf
import streamlit as sl
from numpy.random import default_rng

rng = default_rng(seed=42)


def get_line(m=.6, b=7, n_pts=1000):
    """Values for y = m x + b, on the unit interval.
    """
    return pd.DataFrame(dict(x=x,
                             y=m * x + b)
                        for x in np.linspace(0, 1, n_pts))


def ols(eps=.5):
    """Ordinary Least Squares regression demo.
    """
    df = get_line()
    df.y += eps * rng.standard_normal(size=len(df))

    model = smf.ols('y ~ x', data=df).fit()

    print(model.summary())


if __name__ == '__main__':
    ols()
