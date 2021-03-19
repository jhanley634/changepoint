#! /usr/bin/env streamlit run

# Copyright 2021 John Hanley. MIT licensed.

from time import time

from numpy.random import default_rng
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
        kind = st.radio('kind', ['step', 'ramp'])
        sigma = st.slider('sigma', max_value=4.0, value=1.)
        bkpt = st.slider('breakpoint', 0, n_samples, value=500)
        signal = np.random.normal(0, sigma, n_samples)
        n_after = n_samples - bkpt  # number of samples after the breakpoint
        if kind == 'step':
            signal[bkpt:] += [1] * n_after
        else:
            ramp = np.zeros((bkpt,), dtype='float64')
            ramp = np.pad(ramp, (0, n_after), mode='linear_ramp', end_values=1.0)
            signal += ramp

        results = []
        # detection
        for algo in rpt_algorithms:
            t0 = time()
            bkpt_result = algo(model='rbf').fit(signal).predict(pen=10)
            bkpt_result += [0] * 5  # In case we miss a breakpoint or two.
            msecs = int(1e3 * round(time() - t0, 3))
            d = dict(msecs=msecs, name=algo.__name__)
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
        ax.set_ylim(bottom=-6, top=6)
        ax.legend(loc='upper right')
        st.pyplot(fig)


if __name__ == '__main__':
    Detector.demo4()
