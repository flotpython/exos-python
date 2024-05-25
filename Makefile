#
# run nbprune on all notebooks to produce a version without the corrections
#
# requirements:
# 	make requirements
# - or simply
# 	pip install nbprune
#

all: toc style prune artefacts book-ds book-python
ds: toc style prune artefacts book-ds
python: toc style prune artefacts book-python

include Makefile.style


# PRUNE
SOLUTIONS = $(shell find . -name '*.py' -o -name '*.md' \
  | egrep -- '-corrige\.|\.teacher' \
  | egrep -v '.ipynb_checkpoints|_build')

PRUNEFLAGS = -v

all: prune

prune:
	nbprune $(PRUNEFLAGS) $(SOLUTIONS)

prune-in:
	@ls -1 $(SOLUTIONS)
prune-out-all:
	@nbprune -l $(SOLUTIONS)
prune-out:
	@nbprune -L $(SOLUTIONS)
prune-diff:
	@nbprune -d $(SOLUTIONS)
.PHONY: all prune prune-in prune-out-all prune-out prune-diff


requirements:
	pip install nbprune
.PHONY: requirements


# ARTEFACTS
artefacts:
	find . -name ARTEFACTS | xargs update-artefacts.sh
.PHONY: artefacts


# EXEC
exec:
	./execute-all-notebooks.sh -v
exec-clean:
	./execute-all-notebooks.sh -x -c -v
.PHONY: exec exec-clean

# TOC
# table of contents: inject the contents from both jb tocs into nbhosting
toc: .nbhosting/nbhosting.yaml
.PHONY: toc

.nbhosting/nbhosting.yaml: jb/python/_toc.yml jb/ds/_toc.yml
	$$HOME/git/nbhosting/scripts/jb-to-nbh-toc.py -t data-science jb/ds/_toc.yml "$@"
	$$HOME/git/nbhosting/scripts/jb-to-nbh-toc.py -t python jb/python/_toc.yml "$@"


# BOOKS
book-python:
	PYDEVD_DISABLE_FILE_VALIDATION=1 jupyter-book build --toc jb/python/_toc.yml --config jb/_config.yml --path-output book-python .
book-ds:
	PYDEVD_DISABLE_FILE_VALIDATION=1 jupyter-book build --toc jb/ds/_toc.yml --config jb/_config.yml --path-output book-ds .
book:
	@echo choose the book you want to build
	@echo make book-python
	@echo or
	@echo make book-ds
.PHONY: book-python book-ds book 

book-python-clean:
	rm -rf book-python
book-ds-clean:
	rm -rf book-ds
book-clean: book-python-clean book-ds-clean
.PHONY: book-python-clean book-ds-clean book-clean
