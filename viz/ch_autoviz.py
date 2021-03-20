#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

from autoviz.AutoViz_Class import AutoViz_Class

from viz.pd_prof import get_us_df


if __name__ == '__main__':
    fspec = '/tmp/us.csv'
    df = get_us_df()
    df.to_csv(fspec)

    AV = AutoViz_Class()
    dft = AV.AutoViz('', dfte=df, depVar='deaths', verbose=2, chart_format='png')
