from setuptools import setup
import os
from glob import glob

package_name = "sentinel_oda"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="user",
    maintainer_email="user@example.com",
    description="Sentinel V1 - ODA Package (stub)",
    license="MIT",
    entry_points={
        "console_scripts": [
            "depth_node = sentinel_oda.depth_node:main",
            "detection_node = sentinel_oda.detection_node:main",
            "oda_maneuvers = sentinel_oda.oda_maneuvers:main",
            "inner_map = sentinel_oda.inner_map:main",
        ],
    },
)
