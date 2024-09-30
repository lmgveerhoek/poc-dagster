from setuptools import find_packages, setup

setup(
    name="energiebespaarders",
    packages=find_packages(exclude=["energiebespaarders_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
