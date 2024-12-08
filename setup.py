import ast
import re

from setuptools import setup

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("cbrf/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

print(version)

setup(
    name="cbrf",
    version=version,
    packages=["cbrf", "cbrf.asyncio"],
    install_requires=[
        "requests",
        "aiohttp",
    ],
    url="https://github.com/egregors/cbrf",
    license="MIT",
    author="Vadim Iskuchekov (@egregors)",
    author_email="egregors@pm.me",
    description="Wrapper for The Central Bank of the Russian Federation site API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
)
