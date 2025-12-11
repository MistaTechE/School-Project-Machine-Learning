#shap.py
import shap
import matplotlib.pyplot as plt

def shap_info(df, model):
    features = [
        "2021-2022 attendance rate - year to date_scaled",
        "2020-2021 attendance rate_scaled",
        "2019-2020 attendance rate_scaled",
        "2021-2022 student count - year to date_scaled",
        "2020-2021 student count_scaled",
        "2019-2020 student count_scaled"
    ]

    X = df[features]

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    shap.summary_plot(shap_values, X)
    shap.summary_plot(shap_values, X, plot_type="bar")

    # Beeswarm plot
    plt.figure(figsize=(10,6))
    shap.summary_plot(shap_values, X, show=False)
    plt.tight_layout()
    plt.savefig("data/shap_beeswarm.png", dpi=300)
    plt.close()

    # Bar plot
    plt.figure(figsize=(10,6))
    shap.summary_plot(shap_values, X, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig("data/shap_bar.png", dpi=300)
    plt.close()

    print("SHAP plots saved as 'shap_beeswarm.png' and 'shap_bar.png'")

    #print("printing shap info")
    #print(shap_values)

    return shap_values



