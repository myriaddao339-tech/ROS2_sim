from setuptools import setup
import os
from glob import glob

package_name = "sentinel_mission"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "missions"), glob("missions/*.plan")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="user",
    maintainer_email="user@example.com",
    description="Sentinel V1 - Mission Package",
    license="MIT",
    entry_points={
        "console_scripts": [
            "drone_node = sentinel_mission.drone_node:main",
            "mission_node = sentinel_mission.mission_node:main",
            "emergency_node = sentinel_mission.emergency_node:main",
            "start_trigger = sentinel_mission.start_trigger:main",
        ],
    },
)
