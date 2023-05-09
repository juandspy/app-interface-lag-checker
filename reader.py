import yaml
from yaml.loader import SafeLoader
from typing import Dict
from pprint import pprint

def read_yml(path: str) -> Dict:
    with open(path) as f:
        return yaml.load(f, Loader=SafeLoader)

def get_resources(path: str) -> Dict:
    data = read_yml(path)
    return data["resourceTemplates"]


if __name__ == "__main__":
    resources = get_resources("deploy.yml")
    for resource in resources:
        pprint(resource)
        break