
install:
	@pip install -Ur requirement.txt

build: clean install
	@python3 setup.py sdist bdist_wheel

check: build
	@twine check dist/*

clean:
	@rm -rf dist/ workers/ build/

upload-test:
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	@twine upload dist/*

test-dep:
	@python3 -m pip install --upgrade pip
	@python3 -m pip install --upgrade requests

test: test-dep
	@python3 test.py

.PHONY: install build check clean upload-test upload test test-dep
