from pathlib import Path

from setuptools import setup, find_namespace_packages

from uast.__version__ import __version__

long_description = Path("README.md").read_text()

setup(
  name="uast",
  version=f"{__version__}",
  license="MIT",
  author="Vasco Schiavo",
  author_email="vasco.schiavo@protonmail.com",
  url="https://github.com/VascoSch92/uast",
  description="Uast, user abstract syntax tree, is a",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=find_namespace_packages(include=["uast*"], exclude=["tests"]),
  entry_points={
        "console_scripts": ["uast=uast:main"]
    },
  # download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords=["structure", "testing", "schema", "syntax"],
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
  ],
  python_requires=">=3.9",
)

