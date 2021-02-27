#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

import matplotlib.pyplot as plt
import ruptures as rpt


class Detector:
    """A changepoint detector.

    Consumes (noisy) sample observations,
    and declares that 0, 1, or 2 of them are changepoints.
    """

    @staticmethod
    def demo1():
        """From https://github.com/deepcharles/ruptures"""

        # generate signal
        n_samples, dim, sigma = 1000, 3, 4
        n_bkps = 4  # number of breakpoints
        signal, bkps = rpt.pw_constant(n_samples, dim, n_bkps, noise_std=sigma)

        # detection
        algo = rpt.Pelt(model="rbf").fit(signal)
        result = algo.predict(pen=10)

        # display
        rpt.display(signal, bkps, result)
        plt.show()


if __name__ == '__main__':
    Detector.demo1()
