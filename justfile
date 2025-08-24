init:
	flit init

build:
	pyproject-build

doc:
	corre -i doc/source.md -o README.md
	pandoc README.md -so doc/index.html -d pandoc.yml

publish: build doc
	twine upload dist/*
