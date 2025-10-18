"""
PyRay - Python Game Development Made Simple
Setup configuration for PyRay package
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __version__.py
version = {}
with open(os.path.join("pyray", "__version__.py")) as fp:
    exec(fp.read(), version)

setup(
    name="pyray",
    version=version['__version__'],
    author="PyRay Community",
    author_email="pyray@example.com",
    description="Simple and easy-to-use Python library for game development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Om7035/PyRay",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.5.0",
        "numpy>=1.20.0",
        "Pillow>=9.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
            "sphinx>=5.0.0",
        ],
        "audio": [
            "pydub>=0.25.0",
        ],
        "3d": [
            "moderngl>=5.7.0",
            "PyGLM>=2.5.0",
        ],
        "opencv": [
            "opencv-python>=4.9.0",
        ],
        "matplotlib": [
            "matplotlib>=3.8.0",
        ],
        "moderngl": [
            "moderngl>=5.7.0",
            "PyGLM>=2.5.0",
        ],
        "arcade": [
            "arcade>=3.0.0",
        ],
        "pyglet": [
            "pyglet>=2.0.0",
        ],
        "open3d": [
            "open3d>=0.18.0",
        ],
        "pyvista": [
            "pyvista>=0.43.0",
        ],
        "panda3d": [
            "panda3d>=1.10.0",
        ],
        "tiled": [
            "pytiled-parser>=2.2.0",
        ],
        "jupyter": [
            "ipython>=8.0.0",
            "ipywidgets>=8.0.0",
            "imageio>=2.30.0",
        ],
        "all": [
            "opencv-python>=4.9.0",
            "matplotlib>=3.8.0",
            "moderngl>=5.7.0",
            "PyGLM>=2.5.0",
            "arcade>=3.0.0",
            "pyglet>=2.0.0",
            "open3d>=0.18.0",
            "pyvista>=0.43.0",
            "panda3d>=1.10.0",
            "pytiled-parser>=2.2.0",
            "ipython>=8.0.0",
            "ipywidgets>=8.0.0",
            "imageio>=2.30.0",
            "pydub>=0.25.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pyray-new=pyray.tools.project_generator:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
