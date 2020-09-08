from setuptools import setup


setup(
    name="sanja",
    version="1.0.5",
    description="This module aims to make bringing Jinja templates to Sanic to be easy.",
    long_description_content_type="text/markdown",
    url="https://github.com/tomaszdrozdz/sanja",
    author="tomaszdrozdz",
    author_email="tomasz.drozdz.1@protonmail.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8"],
    py_modules=["sanja"],
    install_requires=["sanic", "jinja2"],
    python_requires='>=3.8')
