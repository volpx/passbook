#!/usr/bin/env python3

#passbook setup.py
from setuptools import setup,find_packages
from passbook.passbook_main import version,author,email
setup(
    name='passbook',
    packages = find_packages(),
    version=version,
    description='Shitty password manager',
    author=author,
    author_email=email,
    license='LICENSE file',
    url='https://github.com/volpx/passbook',
    keywords=['backup','utility','password','manager'],
    #package_data={
        #'ftp_backup.modules':['data/default_configuration_file.cfg']
    #},
    entry_points={
        'console_scripts':[
            'passbook = passbook.passbook_main:main'
        ]
    },
    extras_require={
        'Cryptolib':['pycryptodome']
    }
)
