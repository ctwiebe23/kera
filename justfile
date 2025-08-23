init:
	flit init

build:
	pyproject-build

publish:
	twine upload dist/*

doc:
	corre -i doc/source.md -o README.md
	pandoc README.md -so doc/index.html -d pandoc.yml
