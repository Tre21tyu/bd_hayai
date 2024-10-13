from setuptools import setup, find_packages

setup(
    name="hayai_tool",                  # The name of your tool
    version="0.1",
    packages=find_packages(),
    install_requires=[                  # Dependencies if needed
        "pandas",
        "pyperclip",
        "argparse"
    ],
    entry_points={
        'console_scripts': [
            'hayai=hayai.main:main',    # Maps the 'hayai' command to the 'main' function in your script
        ],
    },
    python_requires='>=3.6',            # Ensure correct Python version
)
