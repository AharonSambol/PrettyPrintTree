to make a new release do:
```bash
python -m pip install --upgrade twine pkginfo setuptools wheel
```
```bash
rm -rf dist/ build/ *.egg-info
```
```bash
python setup.py sdist bdist_wheel
```
```bash
python -m twine check dist/*
```
```bash
python -m twine upload dist/*
```