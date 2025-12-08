#normalize.py
import numpy as np
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def normalize(df):
    #numeric columns
    attendance_cols = [
        "2021-2022 attendance rate - year to date",
        "2020-2021 attendance rate",
        "2019-2020 attendance rate"
    ]

    count_cols = [
        "2021-2022 student count - year to date",
        "2020-2021 student count",
        "2019-2020 student count"
    ]
    #deal with empty columns so there isn't an error with KMeans
    df[attendance_cols] = df[attendance_cols].fillna(0)
    df[count_cols] = df[count_cols].fillna(0)

    #normalize using min–max scale [0,1]
    minmax = MinMaxScaler()
    df[[col + "_scaled" for col in attendance_cols]] = minmax.fit_transform(df[attendance_cols])

    #log1p transform → RobustScaler
    df[count_cols] = np.log1p(df[count_cols])
    robust = RobustScaler()
    df[[col + "_scaled" for col in count_cols]] = robust.fit_transform(df[count_cols])

    #clustering scaled columns
    cluster_features = [c + "_scaled" for c in attendance_cols + count_cols]
    X = df[cluster_features]

    #best k using silhouette score
    best_k = None
    best_score = -1
    for k in range(2, 7):  # test k = 2 to 6
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        labels = km.fit_predict(X)
        score = silhouette_score(X, labels)
        if score > best_score:
            best_k = k
            best_score = score

    print(f"Best k: {best_k}, silhouette score: {best_score:.4f}")

    #fit final model
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init="auto")
    df["performance_cluster"] = kmeans.fit_predict(X)

    print("Normalization + clustering complete. Column added: 'performance_cluster'")
    df.to_csv(f"data/normalized_dataframe.csv", index=False)
    return df