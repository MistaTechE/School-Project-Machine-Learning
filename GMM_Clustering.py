#GMM_Clustering.py

from sklearn.mixture import GaussianMixture
from randomforest import train_explainer_model
from best_rfr_params import rand_search

def gmm_cluster(df):

    # features used for clustering
    cluster_features = [
        "2021-2022 attendance rate - year to date_scaled",
        "2020-2021 attendance rate_scaled",
        "2019-2020 attendance rate_scaled",
        "2021-2022 student count - year to date_scaled",
        "2020-2021 student count_scaled",
        "2019-2020 student count_scaled"
    ]

    X = df[cluster_features]

    # try multiple components to choose best via BIC
    lowest_bic = float("inf")
    best_gmm = None
    best_k = None

    for k in range(2, 7):
        gmm = GaussianMixture(
            n_components=k,
            covariance_type='full',
            random_state=42
        )
        gmm.fit(X)

        bic = gmm.bic(X)
        if bic < lowest_bic:
            lowest_bic = bic
            best_gmm = gmm
            best_k = k

    print(f"Best GMM components: {best_k}")

    # Fit final GMM
    gmm = best_gmm
    df["gmm_cluster"] = gmm.predict(X)
    df["cluster_prob_low_attendance"] = gmm.predict_proba(X).min(axis=1)
    df.to_csv(f"data/gmm_dataframe.csv", index=False)
    #TODO need to use best_model in train_explainer_model
    best_model = rand_search(df)

    model, shap_values = train_explainer_model(df)
    return df, model, shap_values