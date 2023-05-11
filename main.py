import os

from reader import get_resources
from lag_checker import get_lag_from_repo, clone_resource, get_commit_n_days_ago


INPUT_FILE = os.environ.get("INPUT_FILE")
if INPUT_FILE is None:
    print("ERROR: INPUT_FILE environment variable must be set")
    exit(1)

N_DAYS = os.environ.get("N_DAYS", 0)

print("url,name,env_name,lag")

for resource in get_resources(INPUT_FILE):
    url, name = resource["url"], resource["name"]
    repo = clone_resource(url, name)
    # pprint(resource)
    for environment in resource["targets"]:
        env_name, from_sha = environment["namespace"]["$ref"], environment["ref"]
        env_name = env_name.split("/")[-1]
        if from_sha == "internal":
            # skip ephemeral for now
            lag = 0
        else:
            lag = get_lag_from_repo(
                repo, 
                from_sha, 
                to_sha=get_commit_n_days_ago(repo, n_days=N_DAYS)
            )
        print(f"{url},{name},{env_name},{lag}")