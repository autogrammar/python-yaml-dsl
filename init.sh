#!/bin/bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pyyaml
pip install inflect
pip install inflection
rm examples.yaml
python dsl.py dsl.yaml private.yaml public.yaml -n 5 -o examples.yaml
