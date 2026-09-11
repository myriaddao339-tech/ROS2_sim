from setuptools import find_packages, setup
from glob import glob

package_name = 'navigation_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name , glob('launch/*')),
        ('share/' + package_name, glob('missions/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gideon',
    maintainer_email='axel.adje12@gmail.com',
    description='TODO: Package description',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'navigation_node = navigation_pkg.navigation_node:main',
            'offboard_node = navigation_pkg.offboard_node:main',
        ],
    },
)
