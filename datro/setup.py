"""Allows installation when using pip < 21.1."""

from setuptools import setup

setup(
    name="datro",
    include_package_data=True,
    package_data={"datro": ["data/*"]},
)
