from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="MLOps_Housing",
    version="0.1",
    packages=find_packages(),
    author="Anvesh",
    install_requires=requirements
)
