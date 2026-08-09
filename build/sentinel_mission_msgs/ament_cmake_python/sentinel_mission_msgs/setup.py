from setuptools import find_packages
from setuptools import setup

setup(
    name='sentinel_mission_msgs',
    version='0.1.0',
    packages=find_packages(
        include=('sentinel_mission_msgs', 'sentinel_mission_msgs.*')),
)
