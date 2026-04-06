import pandas as pd

def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file, header=None, names=["raw"])

    df["ip"] = df["raw"].str.extract(r'(\d+\.\d+\.\d+\.\d+)')
    df["message"] = df["raw"]

    return df

def ip_analysis(df):
    return df["ip"].value_counts()

def status_analysis(df):
    # 行末の " ... HTTP/1.1" 200 のように、200 の後ろに空白がないログも拾う
    df["status"] = df["raw"].str.extract(r'\s(\d{3})(?:\s|$)')
    return df["status"].value_counts()

def error_logs(df):
    return df[
        df["message"].str.contains(
            "error|failed|denied|invalid|refused",
            case=False,
            na=False
        )
    ]