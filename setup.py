# encoding: utf-8
from setuptools import setup, find_packages
from PyPackman import Packman

setup(
    name='pypackman',
    version=Packman.version,
    author='Christoph Koerner',
    author_email='office@chaosmail.at',
    description='PyPackman creates a virtualenv including all dependencies',
    url='https://github.com/chaosmail/pypackman',
    download_url='https://github.com/chaosmail/pypackman/releases',
    license='MIT License',
    install_requires=['virtualenv==1.11.4', 'pytest==2.5.2'],
    packages=find_packages(),
    include_package_data=True,
    scripts=['bin/packman'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3'
    ],
)
