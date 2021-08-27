clean:
	@rm -rf dist/ workers/ build/ cloudflare_api.egg-info/
	@find . -type d -name *pycache* -exec rm -rf {} +

check: 
	@twine check dist/*

pip-install:
	@python3 -m pip install --upgrade pip > /dev/null
	@pip3 install setuptools wheel

install: pip-install
	@pip3 install -Ur requirement.txt

build: clean
	@python3 setup.py sdist bdist_wheel

publish-test: check
	@twine upload -r testpypi dist/*

publish: check
	@twine upload dist/*

test-dep:
	@python3 -m pip install --upgrade requests > /dev/null

test: test-dep
	@python3 test.py

.PHONY: install build pip-install check clean upload-test upload test test-dep
