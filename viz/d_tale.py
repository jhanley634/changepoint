#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

import dtale

from viz.pd_prof import get_us_df


if __name__ == '__main__':
    d = dtale.show(get_us_df())
