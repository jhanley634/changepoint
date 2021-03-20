#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

from autoviz.AutoViz_Class import AutoViz_Class

from viz.pd_prof import get_us_df


if __name__ == '__main__':

    AV = AutoViz_Class()
    dft = AV.AutoViz('', dfte=get_us_df(), depVar='deaths', verbose=2, chart_format='png')
