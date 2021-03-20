
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
PKGS = pandas-profiling sweetviz xlrd

viz/out/sweet.html:
	$(ACTIVATE) && conda list | grep pandas-profiling || ($(INSTALL) $(PKGS); pip install autoviz)
	$(ACTIVATE) && viz/sweet.py
	$(ACTIVATE) && viz/ch_autoviz.py
	# $(ACTIVATE) && viz/pd_prof.py

auto/foo.txt:
	$(ACTIVATE) && conda list | grep auto-sklearn || $(INSTALL) pyrfr tpot
	$(ACTIVATE) && conda list | grep auto-sklearn || pip install auto-sklearn

EXCLUDE = '/\.(git|idea)/|/__pycache__/|LICENSE|\.(html|pdf|png)$$'
L = --files-without-match
C2021 = 'Copyright 2021 John Hanley\. MIT licensed\.'
audit:
	find . -type f | egrep -v $(EXCLUDE) | sort | xargs egrep $(L) $(C2021)
