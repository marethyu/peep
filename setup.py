import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thepeep",
    version="1.1.2",
    author="Jimmy Yang",
    author_email="codingexpert123@gmail.com",
    description="A toy programming language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marethyu12/peep",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    entry_points = {
        "console_scripts" : [
            "peep=peep.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords = "python programming-language interpreter",
    python_requires='>=3.6',
    zip_safe=True
)