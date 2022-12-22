# JADN Schema

This logic can be added to other projects via the python whl. 

## Setup
1) Setup your virtual environment, if you have not done so
2) run setup.py to pulled down the dependencies and setup the jadnschema whl.
   1) python ./setup.py
3) If you are doing development, then also install the development dependencies.
   1) pip install -r requirements_dev.txt

## How to create the whl
1) Run: python setup.py bdist_wheel --universal
2) Under dist, locate: jadnschema-0.1.0-py2.py3-none-any.whl
3) Copy to the repo or project that requires this functionality
4) To add to the other project run: pip install jadnschema-0.1.0-py2.py3-none-any.whl

## Creating the Docs
1) Run: python mkdocs.py
2) Open docs/index.html
