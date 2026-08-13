from setuptools import find_packages
from setuptools import setup

setup(
    name='sentinel_oda_msgs',
    version='0.1.0',
    packages=find_packages(
        include=('sentinel_oda_msgs', 'sentinel_oda_msgs.*')),
)
