from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='PrettyPrintTree',
    version='1.192',
    author="Aharon Sambol",
    author_email='email@example.com',
    py_modules=find_packages('PrettyPrint'),
    packages=find_packages(),
    license='MIT License',
    url='https://github.com/AharonSambol/PrettyPrintTree',
    keywords=['tree', 'pretty', 'print', 'pretty-print', 'display'],
    description='A tool to print trees to the console',
    long_description=long_description,
    long_description_content_type="text/markdown",

)
