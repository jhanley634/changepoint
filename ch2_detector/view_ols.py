#! /usr/bin/env steamlit run

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import streamlit as sl


def ols(m=1, b=0, eps=.1):
    """Ordinary Least Squares regression demo.

    y = m x + b + epsilon_noise
    """
    dat = sm.datasets.get_rdataset("Guerry", "HistData").data
    print(dat)

    # Fit regression model (using the natural log of one of the regressors)
    results = smf.ols('Lottery ~ Literacy + np.log(Pop1831)', data=dat).fit()

    print(results.summary())



if __name__ == '__main__':
    ols()
