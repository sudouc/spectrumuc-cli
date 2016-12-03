"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('spectrumuc/spectrumuc.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "spectrumuc-cli",
    packages = ["spectrumuc"],
    install_requires=[
        "pyrebase"
    ],
    entry_points = {
        "console_scripts": ['suc = spectrumuc.spectrumuc:main']
        },
    version = version,
    description = "Spectrum UC management cli",
    long_description = long_descr,
    author = "Alisdair Robertson"
    )
