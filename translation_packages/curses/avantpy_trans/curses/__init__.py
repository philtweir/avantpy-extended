import os
import yaml

with open(os.path.join(
        os.path.dirname(__file__),
        'definition.yaml'
        ), 'r') as f:
    definition = yaml.safe_load(f)
