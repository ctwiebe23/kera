# initialize the project
init:
	flit init

# build the project
build:
	pyproject-build

# generate documentation and readme from source
doc:
	corre -i doc/source.md -o README.md
	pandoc README.md -so doc/index.html -d pandoc.yml -d readme
	pandoc CHANGELOG.md -so doc/changelog/index.html -d pandoc.yml -d readme

# clean the project
clean:
	[ -d dist ] && rm -r dist || true

# publish to pypi
publish: clean doc build
	twine upload dist/*
