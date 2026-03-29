import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from analysis import load_data, ip_analysis, status_analysis, error_logs
from anomaly_detection import detect_anomaly

st.title("AI Security Log Analyzer")

st.markdown("""
### 🔍 このツールについて
本ツールは、サーバーログから不正アクセスや異常な通信を検知するために開発しました。

### 🎯 解決する課題
- 大量ログから異常を手動で見つけるのは困難
- 攻撃の兆候を見逃すリスク

### 💡 特徴
- IPごとのアクセス分析
- エラーログ抽出
- AIによる異常検知（IsolationForest）
""")

uploaded_file = st.file_uploader("ログファイルをアップロード", type=["csv"])

st.download_button(
    label="📥 サンプルログをダウンロード",
    data=open("sample_log.csv", "rb").read(),
    file_name="sample_log.csv",
    mime="text/csv"
)

if uploaded_file:

    df = load_data(uploaded_file)

    st.subheader("ログデータ")
    st.dataframe(df)

    # IPランキング
    st.subheader("IPアクセスランキング")

    ip_count = ip_analysis(df)
    st.write(ip_count)

    fig = px.bar(
        x=ip_count.index,
        y=ip_count.values,
        labels={"x":"IP","y":"Access Count"},
        title="IP Access Ranking"
    )

    st.plotly_chart(fig)

    # ステータスコード
    st.subheader("ステータスコード分析")

    status_count = status_analysis(df)

    fig2 = px.pie(
        values=status_count.values,
        names=status_count.index,
        title="Status Code Distribution"
    )

    st.plotly_chart(fig2)

    # エラー
    st.subheader("エラーログ")

    st.dataframe(error_logs(df))

    # AI異常検知
    st.subheader("AI 異常検知")

    anomalies = detect_anomaly(df)

    if not anomalies.empty:
       st.error("⚠️ 異常なアクセスを検知しました！")
    else:
      st.success("✅ 異常は検知されませんでした")

    st.write("怪しいIP")

    st.write("⚠️ 異常と判定されたIP（アクセス頻度が通常と異なる）")
    st.dataframe(anomalies)

