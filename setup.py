#!/usr/bin/env python

import re
from pathlib import Path
from setuptools import setup, find_packages

_version_re = re.compile(r"__version__\s=\s\"(.*)\"")


def main():

    HERE = Path(__file__).parent
    README = (HERE / "README.md").read_text()
    version_file = HERE / "CloudflareAPI/__init__.py"
    version_file = version_file.resolve(strict=True).read_text()
    version = _version_re.search(version_file).group(1)

    setup(
        name='cloudflare-api',
        version=version,
        description='Python client for the Cloudflare v4 API',
        long_description=README,
        long_description_content_type="text/markdown",
        author='Nikhil John',
        author_email='nikhiljohn1010@gmail.com',
        url='https://github.com/nikhiljohn10/cloudflare-api',
        license='MIT',
        packages=find_packages(),
        install_requires=['requests'],
        keywords='cloudflare-api',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9'
        ]
    )


if __name__ == '__main__':
    main()
