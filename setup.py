from setuptools import setup, find_packages

setup(
    name="serialmfg",
    version="1.1.4",
    packages=find_packages(),
    description="This module provides a simple Python interface to interact with the Serial API. It allows you to easily perform common operations such as uploading process data, initializing identifiers, and checking the server connection.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/serialmfg/serial-py",
    author="Devon Copeland",
    author_email="founders@serial.io",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=["requests"],
    include_package_data=True
)
