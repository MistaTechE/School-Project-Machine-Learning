#best_rfr_params.py
import matplotlib
matplotlib.use('Agg')
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.model_selection import cross_val_score, KFold, RandomizedSearchCV
from scipy.stats import randint


def rand_search(df):

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

    #hyperparameter optimization
    param_dist = {
        'n_estimators': randint(100, 500),
        'max_depth': randint(3, 15),
        'min_samples_split': randint(2, 10),
        'min_samples_leaf': randint(1, 5),
        'max_features': ['sqrt', 'log2', None]
    }

    base_model = RandomForestRegressor(random_state=42, n_jobs=-1)

    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    #RandomizedSearchCV for hyperparameter optimization
    rand_search = RandomizedSearchCV(
        estimator=base_model,
        param_distributions=param_dist,
        n_iter=10,
        cv=kf,
        scoring='r2',
        n_jobs=-1,
        random_state=42,
        verbose=1
    )

    rand_search.fit(X, y)

    #best model and predictions
    best_model = rand_search.best_estimator_
    best_params = rand_search.best_params_
    best_score = rand_search.best_score_

    #scores
    mae_scores = -cross_val_score(
        best_model, X, y, cv=kf, scoring='neg_mean_absolute_error', n_jobs=-1
    )

    #info to CSV
    cross_validation_info = pd.DataFrame({
        "Model": ["RandomizedSearchCV"],
        "Best Params": [best_params],
        "Best CV R²": [best_score],
        "R² Score/Mean R²": [best_score],
        "Mean MAE": [mae_scores.mean()],
        "MAE Std Dev": [mae_scores.std()]
    })

    cross_validation_info.to_csv(f"data/best_rfr_params.csv", index=False)

    #print metrics
    print("Best Hyperparameters found:", best_params)
    print(f"Best CV R²: {best_score:.3f}")
    print(f"Mean MAE: {mae_scores.mean():.3f} | Std Dev: {mae_scores.std():.3f}")
    return best_params
