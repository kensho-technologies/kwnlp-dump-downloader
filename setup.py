# Copyright 2020-present Kensho Technologies, LLC.
import codecs
import os

from setuptools import find_packages, setup

# single sourcing package version strategy taken from
# https://packaging.python.org/guides/single-sourcing-package-version


PACKAGE_NAME = "kwnlp_dump_downloader"


def read_file(filename: str) -> str:
    """Read package file as text to get name and version."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, PACKAGE_NAME, filename), "r") as f:
        return f.read()


def find_version() -> str:
    """Only define version in one place."""
    for line in read_file("__init__.py").splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def find_long_description() -> str:
    """Return the content of the README.rst file."""
    return read_file("../README.md")


setup(
    name=PACKAGE_NAME,
    version=find_version(),
    description="Utility for downloading and checking the status of Wikimedia dumps.",
    long_description=find_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/kensho-technologies/kwnlp-dump-downloader",
    author="Kensho Technologies LLC.",
    author_email="kwnlp@kensho.com",
    license="Apache 2.0",
    packages=find_packages(exclude=["tests*"]),
    package_data={"": []},
    install_requires=[
        "dataclasses>=0.7,<1; python_version<'3.7'",
        "requests",
        "wget",
    ],
    extras_require={
        "dev": [
            "pre-commit",
        ]
    },
    entry_points={
        "console_scripts": [
            "kwnlp-get-dump-status=kwnlp_dump_downloader.cli_get_dump_status:main",
            "kwnlp-download-jobs=kwnlp_dump_downloader.cli_download_jobs:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="wikipedia download dump status open data",
    python_requires=">=3.6",
)
