import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

LABEL_SIZE = 10
LEGEND_SIZE = 5
IGNORE_ENVS = ["ocm.yml", "ephemeral-base.yml", "stage-ccx-data-pipeline-stage.yml"]
TITLE = "Difference in commits between stage and production"

def join_results() -> pd.DataFrame:
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "results", "*.csv"))

    joined = pd.DataFrame()

    for f in csv_files:
        df = pd.read_csv(f) 
        df['date'] = os.path.basename(f).rstrip(".csv")
        df['date'] = pd.to_datetime(df['date'], format='%y-%m-%d')

        joined = pd.concat([joined, df])
    return joined

def fill_ax(ax: plt.Axes, title:str):
    # ax.set_xlabel("date",  size = LABEL_SIZE)
    # ax.set_ylabel("lag", size = LABEL_SIZE)
    ax.set_title(title, fontdict={'fontsize':LABEL_SIZE})
    ax.legend(loc="upper right", prop=dict(size=LEGEND_SIZE))

def plot_lag_for_service(df: pd.DataFrame, service: str, ax: plt.Axes, label = ""):
    df = df.copy()
    df = df.loc[df['name'] == service]
    for env in df['env_name'].unique():
        if env in IGNORE_ENVS:
            continue
        data = df.loc[df['env_name'] == env]
        ax.plot(data['date'], data['lag'], label=label)

def plot_grid_of_services(df: pd.DataFrame):
    services = df['name'].unique()
    services = [service for service in services if "grafana" not in service and "mock" not in service]

    fig, axs = plt.subplots(len(services)//2,ncols=2, sharex=True, sharey=False)

    for (ax, service) in zip(axs.flat, services):
        plot_lag_for_service(df, service, ax)
        fill_ax(ax, service)
    
    fig.suptitle(TITLE, fontsize=16)
    return fig

def plot_together(df: pd.DataFrame):
    services = df['name'].unique()
    services = [service for service in services if "grafana" not in service and "mock" not in service]

    fig, ax = plt.subplots(1)

    for service in services:
        plot_lag_for_service(df, service, ax, label=service)
    fill_ax(ax, TITLE)
    return fig

if __name__ == "__main__":
    joined = join_results()
    joined.to_csv("joined.csv", index=False)
    
    joined = pd.read_csv(
        "joined.csv",
        dtype = {'name': str, 'env': str, 'lag': int, 'date': str},
        parse_dates=['date'])

    fig1 = plot_grid_of_services(joined)
    # fig2 = plot_together(joined)
    
    plt.show()
