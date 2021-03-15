#! /usr/bin/env streamlit run

# Copyright 2021 John Hanley. MIT licensed.

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
    def demo1():
        """From https://github.com/deepcharles/ruptures"""
        rpt_algo = st.radio('algorithm', [
            rpt.Binseg,
            rpt.BottomUp,
            rpt.Pelt,
            rpt.Window,
        ])

        # generate signal
        n_samples, dim = 1000, 1
        sigma = st.slider('sigma', max_value=4.0, value=.5)
        n_bkpts = 4  # number of breakpoints
        signal, bkpts = rpt.pw_constant(n_samples, dim, n_bkpts, noise_std=sigma)
        st.write(f'breakpoints at: {SP} ', f', {SP} '.join(map(str, bkpts)))

        # detection
        result = rpt_algo(model='rbf').fit(signal).predict(pen=10)

        df = pd.DataFrame()
        df['signal'] = pd.Series(map(float, signal))
        df['result'] = pd.Series(int(i in result) * 25
                                 for i in range(len(signal)))

        # display
        x = np.arange(len(signal))
        fig, ax = plt.subplots()
        ax.plot(x, df.signal, label='signal')
        ax.plot(x, df.result, label='change point')
        ax.set_ylim(0, 35)
        ax.legend()
        st.pyplot(fig)


if __name__ == '__main__':
    Detector.demo1()
