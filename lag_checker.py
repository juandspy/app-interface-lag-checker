import git
import os
import logging


logging.basicConfig(level=logging.WARN)


def build_path(name: str):
    return os.path.join("/tmp", name)


def clone_resource(url: str, name: str) -> git.Repo:
    path = build_path(name)
    if os.path.exists(path):
        logging.info("Repo %s already exists. Pulling latest version from origin", name)
        repo = git.Repo(path)
        repo.remotes.origin.pull()
        return repo
    else:
        logging.info("Cloning repo %s into %s", name, path)
        return git.Repo.clone_from(url, path)

def get_lag_from_repo(repo: git.Repo, from_sha: str, to_sha: str):
    commits = repo.iter_commits(f"{from_sha}...{to_sha}")
    return sum(1 for _ in commits)

def get_commit_n_days_ago(repo: git.Repo, n_days: int):
    """
    Return $(git rev-list -n1 --before="$N_DAYS days ago" "$BRANCH")
    """
    if n_days == 0:
        return
    branch = repo.active_branch.name
    commit = repo.git.rev_list(f"{branch}", n=1, before=f"{n_days} days ago")
    return commit

if __name__ == "__main__":
    repo = clone_resource("https://gitlab.cee.redhat.com/ccx/ccx-data-pipeline", "ccx-data-pipeline")
    lag = get_lag_from_repo(repo, "958de07e07ff276ce09652a3769e4dccc30bee1d", "9c3ffc2ceff6bba5e2f6662fb743a8442d014a01")
    print(lag)
