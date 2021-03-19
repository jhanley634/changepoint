#! /usr/bin/env streamlit run

# Copyright 2021 John Hanley. MIT licensed.

import statistics

from numpy.random import default_rng
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ruptures as rpt
import streamlit as st

from ch2_adjustable_detector.view_all_det import rpt_algorithms

rng = default_rng(seed=None)


class Detector:
    """A changepoint detector.

    Consumes (noisy) sample observations,
    and declares that 0, 1, or 2 of them are changepoints.
    """

    @staticmethod
    def _get_bkpt_results(n, bkpts, k=20):
        for i in range(n):
            if i - 1 in bkpts:
                yield -k
            elif i in bkpts:
                yield k
            else:
                yield 0

    @classmethod
    def demo4(cls):
        """From https://github.com/deepcharles/ruptures"""

        # generate signal
        n_samples = 1000
        sigma = st.slider('sigma', max_value=11.0, value=1.)
        bkpt = st.slider('breakpoint', 0, n_samples, value=500)
        signal = np.random.normal(0, sigma, n_samples)
        signal[bkpt:] += [1] * (n_samples - bkpt)

        results = []
        # detection
        for algo in rpt_algorithms:
            bkpt_result = algo(model='rbf').fit(signal).predict(pen=10)
            bkpt_result += [0] * 5  # In case we miss a breakpoint or two.
            d = dict(name=algo.__name__)
            for i in range(5):
                d[f'b{i}'] = bkpt_result[i]
            results.append(d)

        results = pd.DataFrame(results)
        st.write(results)

        df = pd.DataFrame()
        df['signal'] = pd.Series(map(float, signal))

        # display
        x = np.arange(len(signal))
        fig, ax = plt.subplots()
        ax.plot(x, df.signal, label='signal')
        ax.set_ylim(bottom=-12, top=12)
        ax.legend(loc='upper right')
        st.pyplot(fig)


if __name__ == '__main__':
    Detector.demo4()
