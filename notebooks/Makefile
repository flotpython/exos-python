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

include Makefile.book
include Makefile.style
include Makefile.prune
include Makefile.toc

# ARTEFACTS
artefacts:
	find . -name ARTEFACTS | xargs update-artefacts.sh
.PHONY: artefacts


# EXEC
exec:
	execute-all-notebooks.sh -v
exec-clean:
	execute-all-notebooks.sh -x -c -v
.PHONY: exec exec-clean
