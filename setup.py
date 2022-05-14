from setuptools import setup, find_packages

setup(
    name='PrettyPrintTree',
    version='1.15',
    author="Aharon Sambol",
    author_email='email@example.com',
    py_modules=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/AharonSambol/PrettyPrintTree',
    keywords=['tree', 'pretty', 'print', 'pretty-print', 'display'],
    description='A tool to print trees to the console',
    long_description='A tool to print trees to the console'
)
