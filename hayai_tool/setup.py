from setuptools import setup, find_packages

setup(
    name="hayai-tool",
    version="0.1.0",
    author="Lonnie Pollocks",
    author_email="lonnieprogramming@gmail.com",
    description="A tool for processing CSV files, generating SQL, and handling templates.",
    url="https://github.com/Tre21tyu/bd_hayai.git",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "pyperclip",
        "openpyxl",
        "argparse",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "hayai=hayai.main:main",
        ],
    },
    python_requires='>=3.6',
)
