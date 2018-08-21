# File: setup.py
# Date: 9-Mar-2018
#
# Update:
#   3-Jul-2018  jdw update CLI entry points and dependencies
#  21-Aug-2018  jdw version adjustments
#
import re

from setuptools import find_packages
from setuptools import setup

packages = []
thisPackage = 'rcsb.db'

with open('rcsb_db/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name=thisPackage,
    version=version,
    description='RCSB Python Database Access and Loading Utility Classes',
    long_description="See:  README.md",
    author='John Westbrook',
    author_email='john.westbrook@rcsb.org',
    url='https://github.com/rcsb/py-rcsb_db',
    #
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
    entry_points={
        'console_scripts': [
            'exdb_repo_load_cli=rcsb_db.exec.RepoLoadExec:main',
            'repo_scan_cli=rcsb_db.exec.RepoScanExec:main',
            'etl_exec_cli=rcsb_db.exec.ETLExec:main',
        ]
    },
    #
    install_requires=['future', 'six', 'python-dateutil', 'pytz', 'mmcif; python_version >= "0.18"', 'scandir; python_version < "3.0"', 'configparser; python_version < "3.0"'],
    packages=find_packages(exclude=['rcsb_db.tests', 'rcsb_db.tests-*', 'tests.*']),
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        '': ['*.md', '*.rst', "*.txt", "*.cfg"],
    },
    #
    # These basic tests require no database services -
    test_suite="rcsb_db.tests",
    tests_require=['tox'],
    #
    # Not configured ...
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    # Added for
    command_options={
        'build_sphinx': {
            'project': ('setup.py', thisPackage),
            'version': ('setup.py', version),
            'release': ('setup.py', version)
        }
    },
    zip_safe=True,
)
