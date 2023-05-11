#!/bin/bash
set -e

REPO_URL="git@gitlab.cee.redhat.com:service/app-interface.git"
REPO_FOLDER="app-interface"
BRANCH="master"
INPUT_FILE="$REPO_FOLDER/data/services/insights/ccx-data-pipeline/deploy.yml"
RESULTS_FOLDER="results"


# Prepare the app-interace repo
if [ -d "$REPO_FOLDER" ];
then
    (
        cd "$REPO_FOLDER"
        git checkout "$BRANCH" 2> /dev/null
        # git pull origin "$BRANCH"  # TODO: uncomment
    )
else
	git clone "$REPO_URL" "$REPO_FOLDER"
fi

mkdir -p "$RESULTS_FOLDER"

checkout_X_days_ago()
{
    N_DAYS=$1
    (
        cd app-interface
        git checkout $(git rev-list -n1 --before="$N_DAYS days ago" "$BRANCH") 2> /dev/null
    )
}

for N_DAYS in {0..365..5}
do
    checkout_X_days_ago "$N_DAYS"
    FILE_NAME="$(date -d "-$N_DAYS days" +"%y-%m-%d").csv"
    echo "Creating $FILE_NAME"
    INPUT_FILE="$INPUT_FILE" N_DAYS="$N_DAYS" python main.py > "$RESULTS_FOLDER/$FILE_NAME"
done
