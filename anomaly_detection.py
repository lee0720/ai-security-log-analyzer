from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomaly(df):

    # IPが取れない行を除外
    df = df.dropna(subset=["ip"])

    ip_counts = df["ip"].value_counts().reset_index()
    ip_counts.columns = ["ip", "count"]

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    ip_counts["anomaly"] = model.fit_predict(ip_counts[["count"]])

    anomalies = ip_counts[ip_counts["anomaly"] == -1]

    return anomalies.sort_values(by="count", ascending=False)