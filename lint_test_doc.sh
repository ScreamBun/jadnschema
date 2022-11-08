#!/usr/bin/env bash

# Lint
pylint --rcfile=.pylintrc --output-format=json jadnschema | pylint-json2html -o lint.html
# Test
python -m unittest -f tests
# Graphviz convert
for gv in $(ls  tests/schema_gen/*.gv); do
  dot -Tpng $gv -o "$gv.png"
done
# Doc
python mkdocs.py