import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-kchisholm", # Replace with your own username
    version="0.0.1",
    author="Kyle Chisholm",
    author_email="dev@kylechisholm.ca",
    description="C/C++ Finite State Machine Template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChisholmKyle/FsmTemplateC",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)