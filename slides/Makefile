
# Copyright 2021 John Hanley. MIT licensed.

OUT = cpd.pdf

all: $(OUT)

%.pdf: %.md
	pandoc -t beamer -H header.tex --pdf-engine=xelatex -o $@ $<

clean:
	rm -f $(OUT)
