
# Copyright 2021 John Hanley. MIT licensed.

all: ci

ci:
	flake8

prepare:
	conda env update

isort:
	isort --ff=yes ch*/*.py


ACTIVATE = source activate changepoint
ENV = env STREAMLIT_SERVER_RUN_ON_SAVE=true

run2:
	$(ACTIVATE) && $(ENV) ch2_adjustable_detector/view_all_det.py

run3:
	$(ACTIVATE) && $(ENV) ch3_generator/view_det.py


INSTALL = conda install -c conda-forge -y
PKGS = pandas-profiling

viz/covid-profile.html:
	$(ACTIVATE) && conda list | grep pandas-profiling || $(INSTALL) $(PKGS)
	viz/pd_prof.py

EXCLUDE = '/\.(git|idea)/|/__pycache__/|LICENSE'
L = --files-without-match
C2021 = 'Copyright 2021 John Hanley\. MIT licensed\.'
audit:
	find . -type f | egrep -v $(EXCLUDE) | sort | xargs egrep $(L) $(C2021)
