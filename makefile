install:
	@pip install -Ur requirement.txt

build: clean install
	@python3 setup.py sdist bdist_wheel

check: 
	@twine check dist/*

clean:
	@rm -rf dist/ workers/ build/ cloudflare_api.egg-info/
	@find . -type d -name *pycache* -exec rm -rf {} +

upload-test: build check
	@twine upload -r testpypi dist/*

upload: build check
	@twine upload dist/*

test-dep:
	@python3 -m pip install --upgrade pip > /dev/null
	@python3 -m pip install --upgrade requests > /dev/null

test: test-dep
	@python3 test.py

.PHONY: install build check clean upload-test upload test test-dep
