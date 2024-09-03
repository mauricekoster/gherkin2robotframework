from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gherkin2robotframework",
    version="0.4",
    packages=["gherkin2robotframework"],
    install_requires=["gherkin-official==29.0.0", "pyyaml==6.0.2"],

    author="Maurice Koster",
    author_email="maurice@mauricekoster.com",
    description="Translate Gherkin feature files into RobotFramework tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="gherkin robotframework",
    url="https://github.com/mauricekoster/gherkin2robotframework/",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',

    entry_points={
        "console_scripts": [
            "gherkin2robotframework = gherkin2robotframework.__main__:main",
            "dumpgherkin = gherkin2robotframework.dumpgherkin:main",
        ],
    }
)
