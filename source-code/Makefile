# This Makefile is used to build a .pdf report file from a LaTex source project

# 2023, Oleksandr Karpenko <karpen04@ads.uni-passau.de>

# SPDX-License-Identifier: MIT

report:
	@echo "Building a report file..."
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex	
clean:
	@echo "Cleaning up cache files..."
	rm *.aux *.log *.out *.bbl *.blg *.pdf
