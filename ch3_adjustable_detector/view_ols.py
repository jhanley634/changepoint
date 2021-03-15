#! /usr/bin/env streamlit run

# Copyright 2021 John Hanley. MIT licensed.

from numpy.random import default_rng
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import streamlit as st

rng = default_rng(seed=None)


def get_line(m=2, b=3, n_pts=1000):
    """Values for y = m x + b, on the unit interval.
    """
    return pd.DataFrame(dict(x=x,
                             y=m * x + b)
                        for x in np.linspace(0, 1, n_pts))


def ols(sigma=.5):
    """Ordinary Least Squares regression demo, with Gaussian noise sigma.
    """
    df = get_line()
    df.y += sigma * rng.standard_normal(size=len(df))

    model = smf.ols('y ~ x', data=df).fit()
    df['predicted_y'] = model.predict()

    params = pd.DataFrame([dict(intercept=model.params.Intercept,
                                slope=model.params.x)])
    st.write(params)

    df.y.clip(upper=6, inplace=True)  # This is convenient for stable y_lim, interactively.
    st.line_chart(df)
    st.write(df)


if __name__ == '__main__':
    ols()
