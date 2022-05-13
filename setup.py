from setuptools import setup, find_packages

setup(
    name='PrettyPrintTree',
    version='1.2',
    author="Aharon Sambol",
    author_email='email@example.com',
    py_modules=find_packages('prettyprinttree'),
    package_dir={'': 'prettyprinttree'},
    url='https://github.com/AharonSambol/PrettyPrintTree',
    keywords=['tree', 'pretty', 'print', 'pretty-print', 'display'],
    description='A tool to print trees to the console'
)
