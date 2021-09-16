VERSION_FILE := $(shell pwd)/CloudflareAPI/__version__.py
CURRENT_VERSION := $(subst #v,,$(shell cat $(VERSION_FILE)))

version:
	@echo "cloudflare-api v$(CURRENT_VERSION)"

clean:
	@rm -rf dist/ downloads/ build/ *.egg-info/
	@find . -type d -name *pycache* -exec rm -rf {} +

init:
	@python3 -m venv venv

check: 
	@twine check dist/*

pip-install:
	@python3 -m pip install --upgrade pip > /dev/null 2>&1
	@python3 -m pip install setuptools wheel > /dev/null 2>&1

install: pip-install
	@python3 -m pip install -Ur requirement.txt

build: clean install
	@python3 setup.py sdist bdist_wheel

local: build
	@-pip3 uninstall -y cloudflare_api
	@pip3 install ./dist/cloudflare-api-$(CURRENT_VERSION).tar.gz

publish: check
	@twine upload dist/*

test: local
	@clear && python examples/advanced.py

bump:
ifeq ($(VERSION),)
	@echo "Error: Require VERSION variable to be set."
else ifeq ($(VERSION),$(CURRENT_VERSION))
	@echo "Error: You have given current version as input. Please try again."
else
	@echo "#v$(VERSION)" > $(VERSION_FILE)
	@echo "Bumpping version from $(CURRENT_VERSION) to $(VERSION)"
	@git add .
	@git commit -m "bump version to v$(VERSION)"
	@git tag -a "v$(VERSION)" HEAD -m "cloudflare-api v$(VERSION)"
	@git push --follow-tags
endif

.PHONY: version clean init check pip-install install build local publish test bump
