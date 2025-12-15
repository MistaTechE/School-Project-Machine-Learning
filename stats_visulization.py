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

    #create the cross-tab
    cluster_category_crosstab = pd.crosstab(
        normalized_dataframe['performance_cluster'],
        normalized_dataframe['Category: Student Group']
    )
    print(cluster_category_crosstab)
    cluster_category_crosstab.to_csv("data/cluster_category.csv")


    #normalize by cluster size per row
    cluster_category_percent = cluster_category_crosstab.div(cluster_category_crosstab.sum(axis=1), axis=0) * 100
    #round to 1 decimal for readability
    cluster_category_percent = cluster_category_percent.round(1)
    print(cluster_category_percent)
    cluster_category_percent.to_csv("data/cluster_category_percentages_by_row.csv")


    #normalize by column (category)
    cluster_category_col_percent = cluster_category_crosstab.div(cluster_category_crosstab.sum(axis=0), axis=1) * 100
    #round to 1 decimal
    cluster_category_col_percent = cluster_category_col_percent.round(1)
    print(cluster_category_col_percent)
    cluster_category_col_percent.to_csv("data/cluster_category_percentages_by_column.csv")


def gmm_cluster_summary(normalized_dataframe):
    cluster_cols = [
        '2021-2022 attendance rate - year to date_scaled',
        '2020-2021 attendance rate_scaled',
        '2019-2020 attendance rate_scaled',
        '2021-2022 student count - year to date_scaled',
        '2020-2021 student count_scaled',
        '2019-2020 student count_scaled'
    ]

    #group by cluster and compute stats
    cluster_summary = normalized_dataframe.groupby('gmm_cluster')[cluster_cols].agg(
        ['mean', 'min', 'max', 'count']
    )

    #flatten multi-level columns
    cluster_summary.columns = ['_'.join(col).strip() for col in cluster_summary.columns.values]
    cluster_summary.to_csv("data/gmm_cluster_summary.csv", index=True)
    print("printing gmm cluster summary:")
    print(cluster_summary)

    #create the cross-tab
    cluster_category_crosstab = pd.crosstab(
        normalized_dataframe['gmm_cluster'],
        normalized_dataframe['Category: Student Group']
    )
    print(cluster_category_crosstab)
    cluster_category_crosstab.to_csv("data/gmm_cluster_category.csv")


    #normalize by cluster size per row
    crosstab_percent_row = cluster_category_crosstab.div(cluster_category_crosstab.sum(axis=1), axis=0) * 100
    #round to 1 decimal for readability
    crosstab_percent_row = crosstab_percent_row.round(1)
    crosstab_percent_row.to_csv("data/gmm_category_percentages_by_row.csv")


    #normalize by column (category)
    crosstab_percent_column = cluster_category_crosstab.div(cluster_category_crosstab.sum(axis=0), axis=1) * 100
    #round to 1 decimal
    crosstab_percent_column = crosstab_percent_column.round(1)
    crosstab_percent_column.to_csv("data/gmm_category_percentages_by_column.csv")



def gmm_info(df):
    features = [
        "2021-2022 attendance rate - year to date_scaled",
        "2020-2021 attendance rate_scaled",
        "2019-2020 attendance rate_scaled",
        "2021-2022 student count - year to date_scaled",
        "2020-2021 student count_scaled",
        "2019-2020 student count_scaled"
    ]

    #
    # #cluster averages for numeric features
    # cluster_averages = df.groupby("gmm_cluster")[features].mean()
    # cluster_averages.index.name = "Cluster"
    # cluster_averages["Metric Type"] = "Average (Scaled)"
    #
    # #column-wise percentages for student group composition
    # crosstab = pd.crosstab(df['Category: Student Group'], df["gmm_cluster"])
    # crosstab_percent = crosstab.div(crosstab.sum(axis=0), axis=1) * 100
    # crosstab_percent = crosstab_percent.T
    # crosstab_percent.index.name = "Cluster"
    # crosstab_percent["Metric Type"] = "Percentage of Student Group"
    #
    #
    # #combine averages and composition
    # combined = pd.concat([cluster_averages, crosstab_percent], axis=0, sort=False)
    #
    #TODO trying this out instead:
    # Cluster averages for numeric features
    cluster_averages = df.groupby("gmm_cluster")[features].mean()

    # 2️⃣ Column-wise percentages for student group composition
    crosstab = pd.crosstab(df['Category: Student Group'], df["gmm_cluster"])
    crosstab_percent = crosstab.div(crosstab.sum(axis=0), axis=1) * 100

    # Transpose so clusters are rows
    crosstab_percent = crosstab_percent.T

    # 3️⃣ Combine averages and percentages into a single row per cluster
    combined = pd.concat([cluster_averages, crosstab_percent], axis=1)

    # 4️⃣ Optional: sort columns so numeric features come first
    combined = combined[features + [col for col in combined.columns if col not in features]]






    combined.to_csv("data/final_gmm_info.csv")

    return combined


def summarize_avg_gmm_clusters(df):
    # Attendance features (scaled)
    attendance_cols = [
        "2019-2020 attendance rate_scaled",
        "2020-2021 attendance rate_scaled",
        "2021-2022 attendance rate - year to date_scaled"
    ]

    # Student count features (scaled)
    student_count_cols = [
        "2019-2020 student count_scaled",
        "2020-2021 student count_scaled",
        "2021-2022 student count - year to date_scaled"
    ]

    # Average attendance per row (across years)
    df["avg_attendance_scaled"] = df[attendance_cols].mean(axis=1)

    # Average student count per row (across years)
    df["avg_student_count_scaled"] = df[student_count_cols].mean(axis=1)

    # One row per cluster
    cluster_summary = (
        df
        .groupby("gmm_cluster")[["avg_attendance_scaled", "avg_student_count_scaled"]]
        .mean()
        .reset_index()
    )

    # Save for reporting
    cluster_summary.to_csv("data/gmm_cluster_avg_summary.csv", index=False)

    return cluster_summary




