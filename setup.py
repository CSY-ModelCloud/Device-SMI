from setuptools import setup, find_packages

setup(
    name="device-smi",
    version="0.0.0-dev",
    author= "ModelCloud",
    author_email= "qubitium@modelcloud.ai",
    description= "It's designed to retrieve system information about devices.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ModelCloud/Device-SMI/",
    packages=find_packages(),
    install_requires=[],
    platform = ["linux"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
