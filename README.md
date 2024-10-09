# python-yaml-dsl
DSL builder based on yaml specifications
Save your YAML specification in a file, for example, 
dsl.yaml.

Run the script from the command line, 
specifying the YAML file and optionally the number of examples:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pyyaml inflect yaml
```

```bash
python dsl.py object.yaml private.yaml public.yaml -n 5 -o examples.yaml
python dsl.py email/object.yaml email/private.yaml email/public.yaml -n 5 -o email/examples.yaml
python -m unittest test_dsl.py
```

## TODO
- unit test
- priv repo 
- 
- 