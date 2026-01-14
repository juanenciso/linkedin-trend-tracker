# LinkedIn Post Trend Tracker (Streamlit)

A small Streamlit dashboard that estimates whether a LinkedIn post is taking off (Normal / Despegando / Viral)
using time-series snapshots (impressions, reactions, comments, shares).

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Add some snapshots
python scripts/add_snapshot.py --impressions 200 --reactions 10 --comments 1 --shares 0
python scripts/add_snapshot.py --impressions 350 --reactions 18 --comments 3 --shares 1
python scripts/add_snapshot.py --impressions 620 --reactions 35 --comments 7 --shares 4

streamlit run app/dashboard.py

