#! /usr/bin/env streamlit run

# Copyright 2021 John Hanley. MIT licensed.

import statistics

from numpy.random import default_rng
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ruptures as rpt
import streamlit as st

rng = default_rng(seed=None)
SP = ' &nbsp; &nbsp; '


class Detector:
    """A changepoint detector.

    Consumes (noisy) sample observations,
    and declares that 0, 1, or 2 of them are changepoints.
    """

    @staticmethod
    def _get_averages(signal, bkpts):
        assert bkpts[0] > 0, bkpts
        i = 0
        for regime_idx in bkpts:
            mean = statistics.mean(signal[i:regime_idx])
            while i < regime_idx:
                yield mean
                i += 1

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
    def demo3(cls):
        """From https://github.com/deepcharles/ruptures"""
        rpt_algorithms = [
            rpt.Binseg,
            rpt.BottomUp,
            rpt.Pelt,
            rpt.Window,
        ]

        # generate signal
        n_samples, dim = 1000, 1
        sigma = st.slider('sigma', max_value=4.0, value=.5)
        n_bkpts = 4  # number of breakpoints
        signal, bkpts = rpt.pw_constant(n_samples, dim, n_bkpts, noise_std=sigma)
        st.write(f'breakpoints at: {SP} ', f', {SP} '.join(map(str, bkpts)))

        results = []
        # detection
        for algo in rpt_algorithms:
            bkpt_result = algo(model='rbf').fit(signal).predict(pen=10)
            bkpt_result += [0, 0, 0, 0, 0]  # In case we miss a breakpoint or two.
            d = dict(name=algo.__name__)
            for i in range(5):
                d[f'b{i}'] = bkpt_result[i]
            results.append(d)

        results = pd.DataFrame(results)
        st.write(results)

        df = pd.DataFrame()
        df['signal'] = pd.Series(map(float, signal))
        df['avg'] = pd.Series(cls._get_averages(df.signal, bkpts))
        df['result'] = pd.Series(cls._get_bkpt_results(len(df.signal), set(bkpt_result)))
        assert len(df) == len(df.signal)
        assert len(df) == len(df.avg)
        assert len(df) == len(df.result)
        print(df.avg)

        # display
        x = np.arange(len(signal))
        fig, ax = plt.subplots()
        ax.plot(x, df.signal, label='signal')
        ax.plot(x, df.avg, label='mean')
        ax.plot(x, df.result, label='change point')
        ax.set_ylim(bottom=-37, top=37)
        ax.legend(loc='upper right')
        st.pyplot(fig)


if __name__ == '__main__':
    Detector.demo3()
