#randomforest.py

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from shap_info import shap_info

def train_explainer_model(df):

    features = [
        "2021-2022 attendance rate - year to date_scaled",
        "2020-2021 attendance rate_scaled",
        "2019-2020 attendance rate_scaled",
        "2021-2022 student count - year to date_scaled",
        "2020-2021 student count_scaled",
        "2019-2020 student count_scaled"
    ]

    X = df[features]
    y = df["gmm_cluster"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=400,
        random_state=42
    )

    model.fit(X_train, y_train)

    print("RF accuracy:", model.score(X_test, y_test))

    shap_values = shap_info(df, model)

    return model, shap_values

