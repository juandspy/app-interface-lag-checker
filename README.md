# App Interface Lag Checker

Download any `deploy.yml` file from app-interface like 
[ccx-data-pipeline/deploy.yml](https://gitlab.cee.redhat.com/service/app-interface/-/blob/master/data/services/insights/ccx-data-pipeline/deploy.yml)
and run

```
python main.py > results.csv
```

If the file name is different than `deploy.yml`, rename the file or modify the
variable in [main.py](main.py).