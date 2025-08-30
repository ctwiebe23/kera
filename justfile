init:
	flit init

build:
	pyproject-build

doc:
	corre -i doc/source.md -o README.md
	pandoc README.md -so doc/index.html -d pandoc.yml -d readme

clean:
	[ -d dist ] && rm -r dist || true

publish: clean doc build
	twine upload dist/*
