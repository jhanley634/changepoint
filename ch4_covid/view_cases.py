#! /usr/bin/env streamlit run

# Copyright 2021 John Hanley. MIT licensed.

from pathlib import Path

from numpy.random import default_rng
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from ch2_adjustable_detector.view_all_det import rpt_algorithms

rng = default_rng(seed=None)


class CaseDetector:
    """A changepoint detector for covid case rates.
    """

    @staticmethod
    def _get_deltas(s: pd.Series):
        # cf diff(): https://numpy.org/doc/stable/reference/generated/numpy.diff.html
        prev = s[0]
        for val in s:
            yield float(val - prev)
            prev = val

    @staticmethod
    def _get_us_csv_fspec():
        nyt_repo = Path(__file__ + '/../../../covid-19-data').resolve()
        return nyt_repo / 'us.csv'

    @classmethod
    def demo5(cls):

        kind = st.radio('kind', ['raw', 'delta'])

        df = pd.read_csv(cls._get_us_csv_fspec())

        daily_cases = np.array(list(cls._get_deltas(df.cases)))
        df['daily_cases'] = daily_cases

        daily_deaths = np.array(list(cls._get_deltas(df.deaths)))
        df['daily_deaths'] = daily_deaths

        rate = np.array(list(cls._get_deltas(df.daily_deaths)))
        df['rate'] = rate

        results = []
        # detection
        for algo in rpt_algorithms:
            bkpt_result = algo(model='rbf').fit(daily_cases).predict(pen=10)
            bkpt_result += [0] * 10  # In case we miss the occasional breakpoint.
            d = dict(name=algo.__name__)
            for i in range(8):
                d[f'b{i}'] = bkpt_result[i]
            results.append(d)
        results = pd.DataFrame(results)
        st.write(results)

        # display
        fig, ax = plt.subplots()
        if kind == 'raw':
            df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d').copy()
            ax.plot(df.date, df.cases, label='cases')
            ax.plot(df.date, df.deaths, label='deaths')
        else:
            df['date'] = list(range(len(df.date)))
            ax.plot(df.date, df.daily_cases, label='daily cases')
            ax.plot(df.date, df.daily_deaths, label='daily deaths')
            ax.plot(df.date, df.rate, label='2nd derivative')
        ax.legend(loc='upper right')
        st.pyplot(fig)

        st.write(df)


if __name__ == '__main__':
    CaseDetector.demo5()
