SPHINXOPTS    ?= 
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean html api

clean:
	rm -rf $(BUILDDIR)/*
	rm -f modules.rst app.rst db.rst handlers.rst main.rst metrics.rst parsers.rst

api:
	sphinx-apidoc -f -M -o . ../app

html: api
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)