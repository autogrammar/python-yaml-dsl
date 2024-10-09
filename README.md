# python-yaml-dsl
DSL builder based on yaml specifications
Save your YAML specification in a file, for example, 
dsl.yaml.

Run the script from the command line, 
specifying the YAML file and optionally the number of examples:

```bash
python dsl.py dsl.yaml -n 10
```

Generated 10 examples:
1. connect to Account with Credentials
2. read Message from sender Account
3. delete all Message from email Account
4. disconnect Account
5. create Message from content Email Account
...