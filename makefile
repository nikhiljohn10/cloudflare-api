VERSION_FILE := $(shell pwd)/CloudflareAPI/__version__.py
CURRENT_VERSION := $(subst \#v,,$(shell cat $(VERSION_FILE)))

version:
	@echo "cloudflare-api v$(CURRENT_VERSION)"

clean:
	@rm -rf dist/ workers/ build/ cloudflare_api.egg-info/
	@find . -type d -name *pycache* -exec rm -rf {} +

check: 
	@twine check dist/*

pip-install:
	@python3 -m pip install --upgrade pip > /dev/null 2>&1
	@pip3 install setuptools wheel > /dev/null 2>&1

install: pip-install
	@pip3 install -Ur requirement.txt

build: clean
	@python3 setup.py sdist bdist_wheel

publish-test: check
	@twine upload -r testpypi dist/*

publish: check
	@twine upload dist/*

test-dep: pip-install
	@python3 -m pip install --upgrade requests > /dev/null 2>&1

test: test-dep
	@python3 test.py

bump:
ifeq ($(VERSION),)
	@echo "Error: Require VERSION variable set."
else ifeq ($(VERSION),$(CURRENT_VERSION))
	@echo "Error: You have given current version as input. Please try again."
else
	@echo "#v$(VERSION)" > $(VERSION_FILE)
	@git checkout main
	@echo $(VERSION)
	@git tag $(VERSION)
	@git push --tags
endif

.PHONY: install build pip-install check clean upload-test upload test test-dep version bump
