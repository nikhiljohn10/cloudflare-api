#!/usr/bin/env python

import re
from pathlib import Path
from setuptools import setup, find_packages

_version_re = re.compile(r"__version__\s=\s'(.*)'")


def main():

    cd = Path(".")
    readme = cd / "README.md"
    readme.resolve(strict=True)
    long_description = readme.read_text()
    version_file = cd / "CloudflareAPI/__init__.py"
    version_file.resolve(strict=True)
    version = _version_re.search(version_file.read_text()).group(1)

    setup(
        name='cloudflare-api',
        version=version,
        description='Python wrapper for the Cloudflare v4 API',
        long_description=long_description,
        author='Nikhil John',
        author_email='nikhiljohn1010@gmail.com',
        url='https://github.com/nikhiljohn10/pycf',
        license='MIT',
        packages=find_packages(),
        include_package_data=True,
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