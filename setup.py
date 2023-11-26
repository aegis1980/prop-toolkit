"""
Jon R 
May 2022
"""
from setuptools import setup, find_packages
import os

MY_PACKAGE_NAME = 'prop_toolkit'

def package_files(directory):
    """
    For getting paths of data (non python) files.
    Recursively searches directory
    """
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


assets = package_files(os.path.join(''))

# could possible add other data files here for install to andromeda
# e.g. csv files etc
# other add them to the app folder in andromeda (probably easier!)


setup(
    name=MY_PACKAGE_NAME, 
    install_requires=[
        "numpy","pybemt", "scipy", "icecream"
    ],
    version='0.1', 
    packages=find_packages(),
    include_package_data=True,
    #package_data={
    #    "": assets,
    #}
)