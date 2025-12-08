#stats_visulization.py
import pandas as pd

def cluster_summary(normalized_dataframe):
    cluster_cols = [
        '2021-2022 attendance rate - year to date_scaled',
        '2020-2021 attendance rate_scaled',
        '2019-2020 attendance rate_scaled',
        '2021-2022 student count - year to date_scaled',
        '2020-2021 student count_scaled',
        '2019-2020 student count_scaled'
    ]

    #group by cluster and compute stats
    cluster_summary = normalized_dataframe.groupby('performance_cluster')[cluster_cols].agg(
        ['mean', 'min', 'max', 'count']
    )

    #flatten multi-level columns
    cluster_summary.columns = ['_'.join(col).strip() for col in cluster_summary.columns.values]
    cluster_summary.to_csv("data/cluster_summary.csv", index=True)
    print("printing cluster summary:")
    print(cluster_summary)