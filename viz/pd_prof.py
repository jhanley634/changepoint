#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

import os

from pandas_profiling.profile_report import ProfileReport
import pandas as pd

from ch4_covid.view_cases import get_covid_repo


def _verify_cwd():
    os.chdir('../changepoint')  # Invoke from top level, please, e.g. with make covid.pdf


def get_us_df():
    _verify_cwd()
    df = pd.read_csv(get_covid_repo() / 'us.csv')
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d')
    return df


if __name__ == '__main__':
    profile = ProfileReport(get_us_df())
    with open('viz/out/profile.html', 'w') as fout:
        fout.write(profile.to_html())
