from setuptools import setup, find_packages

setup(
    name="csv_excel_tool",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "argparse",
        "pyperclip",
        "openpyxl",  # Required for reading Excel files with pandas
    ],
    entry_points={
        'console_scripts': [
            'csv_excel_tool=your_script_name:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for processing CSV files, converting Excel to CSV, and generating SQL commands.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://yourprojecturl.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
