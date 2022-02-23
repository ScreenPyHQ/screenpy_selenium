from os import path

from setuptools import find_packages, setup

requires = [
    "screenpy>=4.0.0",
    "screenpy_pyotp>=4.0.0,<4.1",
    "typing-extensions>=4.1.1,<4.2",
    "selenium>=4.1.0,<4.2",
]

repo_dir = path.abspath(path.dirname(__file__))
about = {}
with open(path.join(repo_dir, "screenpy_selenium", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    package_data={"screenpy_selenium": ["py.typed"]},
    packages=find_packages(),
    install_requires=requires,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: BDD",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
    ],
)
