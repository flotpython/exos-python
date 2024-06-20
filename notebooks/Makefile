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

# specific to exos
include Makefile.artefacts
include Makefile.exec
