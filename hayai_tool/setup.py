from setuptools import setup, find_packages

setup(
    name='hayai',
    version='0.1.0',
    packages=find_packages(),
    package_data={
        'ht': ['data/hayai_art.txt'],
    },
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
            "hayai=ht.main:main",
        ],
    },
    author='Lonnie Pollocks',
    author_email='lonnieprogramming@gmail.com',
    description='A utility script for processing CSV and generating SQL',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
)
