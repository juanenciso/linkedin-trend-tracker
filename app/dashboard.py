import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
from core.scoring import trend_score


st.set_page_config(page_title="LinkedIn Trend Tracker", layout="wide")
st.title("📈 LinkedIn Post Trend Tracker")

DATA_PATH = "data/post_timeseries.csv"

st.sidebar.header("Data source")
st.sidebar.write(f"Using: `{DATA_PATH}`")

try:
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
except FileNotFoundError:
    st.error(f"File not found: {DATA_PATH}. Create it in /data.")
    st.stop()

if df.empty:
    st.warning("No data yet. Add a few snapshots.")
    st.stop()

df = df.sort_values("timestamp").reset_index(drop=True)

# Deltas
df["delta_impressions"] = df["impressions"].diff()
df["delta_minutes"] = df["timestamp"].diff().dt.total_seconds() / 60
df.loc[df["delta_minutes"] <= 0, "velocity"] = 0

# Avoid division by zero / negative deltas
df["velocity"] = df["delta_impressions"] / df["delta_minutes"]
df.loc[df["delta_minutes"] <= 0, "velocity"] = 0

# Smooth velocity (rolling mean)
df["velocity_smooth"] = (
    df["velocity"]
    .rolling(window=3, min_periods=1)
    .mean()
)

# Rates
df["engagement_rate"] = (df["reactions"] + df["comments"] + df["shares"]) / df["impressions"].clip(lower=1)
df["share_rate"] = df["shares"] / df["impressions"].clip(lower=1)

current = df.iloc[-1]

baseline = {
    "velocity_mean": df["velocity"].dropna().mean(),
    "velocity_std": df["velocity"].dropna().std(ddof=0) if len(df["velocity"].dropna()) > 1 else 0,
    "engagement_mean": df["engagement_rate"].mean(),
    "engagement_std": df["engagement_rate"].std(ddof=0) if len(df["engagement_rate"]) > 1 else 0,
    "share_mean": df["share_rate"].mean(),
    "share_std": df["share_rate"].std(ddof=0) if len(df["share_rate"]) > 1 else 0,
}

score = trend_score(
    current={
        "velocity": float(current["velocity"]) if pd.notna(current["velocity"]) else 0.0,
        "engagement_rate": float(current["engagement_rate"]),
        "share_rate": float(current["share_rate"]),
    },
    baseline=baseline,
)

# State
if score > 2:
    state = "🚀 Viral"
elif score > 1:
    state = "⚡ Despegando"
else:
    state = "✅ Normal"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Trend Score", score)
c2.metric("Estado", state)
c3.metric("Impresiones", int(current["impressions"]))
c4.metric("Engagement rate", f"{current['engagement_rate']*100:.2f}%")

st.subheader("Time series")
st.subheader("Impressions over time")
st.line_chart(df.set_index("timestamp")[["impressions"]])

st.subheader("Velocity (impressions per minute)")
st.line_chart(df.set_index("timestamp")[["velocity"]])

with st.expander("Ver tabla de snapshots"):
    st.dataframe(df)

