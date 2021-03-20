#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

from sweetviz import analyze

from viz.pd_prof import get_us_df


if __name__ == '__main__':
    a = analyze(get_us_df())
    a.show_html('viz/out/sweet.html', open_browser=False)
