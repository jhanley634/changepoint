#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

import os

import pandas as pd
from pandas_profiling.profile_report import ProfileReport

from ch4_covid.view_cases import get_covid_repo


class Profiler:
    """Profiles the NYTimes covid dataset.
    """

    @classmethod
    def demo6(cls):

        df = pd.read_csv(get_covid_repo() / 'us.csv')
        df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d')
        profile = ProfileReport(df)
        with open('viz/covid-profile.html', 'w') as fout:
            fout.write(profile.to_html())


if __name__ == '__main__':
    os.chdir('../changepoint')  # Invoke from top level, please, e.g. with make covid.pdf
    Profiler.demo6()
