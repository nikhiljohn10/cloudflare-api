install:
	@pip install -Ur requirement.txt

build: clean install
	@python3 setup.py sdist bdist_wheel

check: 
	@twine check dist/*

clean:
	@rm -rf dist/ workers/ build/

upload-test: build check
	@twine upload -r testpypi dist/*

upload: build check
	@twine upload dist/*

test-dep:
	@python3 -m pip install --upgrade pip
	@python3 -m pip install --upgrade requests

test: test-dep
	@python3 test.py

.PHONY: install build check clean upload-test upload test test-dep
