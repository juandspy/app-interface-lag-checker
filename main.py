from reader import get_resources
from lag_checker import get_lag_from_repo, clone_resource


print("url,name,env_name,lag")

for resource in get_resources("deploy.yml"):
    url, name = resource["url"], resource["name"]
    repo = clone_resource(url, name)
    # pprint(resource)
    for environment in resource["targets"]:
        env_name, from_sha = environment["namespace"]["$ref"], environment["ref"]
        env_name = env_name.split("/")[-1]
        if from_sha == "internal":
            # skip ephemeral for now
            lag = "-"
        else:
            lag = get_lag_from_repo(repo, from_sha, to_sha=repo.active_branch)
        print(f"{url},{name},{env_name},{lag}")