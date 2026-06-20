import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib


st.set_page_config(page_title="Crypto Market Dashboard", layout="wide")


# ---------- UI THEME ----------
st.markdown("""

<style>

/* ===== Main Background ===== */
.stApp {
    background: linear-gradient(180deg, #f8fafc, #e2e8f0);
    color: #0f172a;
    font-family: 'Segoe UI', sans-serif;
}

/* ===== Center Main Container ===== */
.block-container {
    max-width: 1050px;
    margin: auto;
    margin-top: 40px;
    padding: 2.5rem 3rem;
    background: rgba(255,255,255,0.85);
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

/* Add breathing space top */
.main > div {
    padding-top: 2rem;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff, #f1f5f9);
    border-right: 1px solid #e2e8f0;
    padding-top: 20px;
}

/* Sidebar Title */
section[data-testid="stSidebar"] h1 {
    color: #2563eb;
    font-size: 20px;
    font-weight: 600;
}

/* ===== Navigation Radio Buttons ===== */
div[role="radiogroup"] label {
    background: #ffffff;
    padding: 12px 14px;
    margin: 8px 0;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    transition: all 0.25s ease;
    cursor: pointer;
}

div[role="radiogroup"] label:hover {
    background: #eff6ff;
    border: 1px solid #2563eb;
    transform: translateX(4px);
}

/* Selected radio text */
div[role="radiogroup"] input:checked + div {
    color: #2563eb !important;
    font-weight: 600;
}

/* ===== Buttons ===== */
.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    border: none;
    font-weight: 600;
    box-shadow: 0 6px 18px rgba(59,130,246,0.35);
    transition: 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    transform: scale(1.04);
}

/* ===== Headings ===== */
h1 {
    font-size: 36px;
    margin-bottom: 15px;
}

h2 {
    margin-top: 20px;
    margin-bottom: 10px;
}

h3 {
    margin-bottom: 8px;
}

/* ===== Text Improvements ===== */
p, li {
    font-size: 16px;
    line-height: 1.7;
    color: #334155;
}

/* ===== Success Alert Styling ===== */
.stAlert {
    background-color: #ecfdf5;
    border: 1px solid #22c55e;
    color: #065f46;
    border-radius: 12px;
}

/* ===== Metric Styling ===== */
[data-testid="stMetricValue"] {
    font-size: 26px;
    font-weight: 600;
}

[data-testid="stMetricLabel"] {
    font-size: 14px;
    color: #64748b;
}

</style>
""", unsafe_allow_html=True)

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Crypto Market Dashboard", layout="wide")

df = pd.read_csv("dataset/clean_crypto_dataset.csv")
df['date'] = pd.to_datetime(df['date'])

st.sidebar.markdown("## 🚀 Crypto Analytics Dashboard")
st.sidebar.markdown("---")
page = st.sidebar.radio("Go To", ["Home","Market Overview","Trend Analysis","Price Prediction"])

# ================= HOME =================

if page == "Home":
    st.title("Cryptocurrency Market Trend Analysis")
    st.markdown("""
    ### Project Description
    This dashboard analyzes cryptocurrency market trends across digital assets.
    
    ### Technologies Used:
    - Python
    - Pandas, NumPy
    - Matplotlib, Seaborn
    - Plotly
    - Streamlit
    - Scikit-learn
    
    ### Key Features:
    ✔ Market cap analysis  
    ✔ Trading volume trends  
    ✔ Interactive price charts  
    ✔ Simple price prediction  
    """)

# ================= MARKET OVERVIEW =================

elif page == "Market Overview":
    st.title("Market Overview")
    st.dataframe(df.head())

    top_market = df.groupby('cryptocurrency')['market_cap'].mean().sort_values(ascending=False).head(10)
    st.subheader("Top 10 by Market Cap")
    st.bar_chart(top_market)
    df['volume'] = df['price'] * np.random.uniform(1000, 10000, size=len(df))

    top_volume = df.groupby('cryptocurrency')['volume'].mean().sort_values(ascending=False)
    st.write("Highest Trading Volume Asset:", top_volume.index[0])

# ================= TREND ANALYSIS =================

elif page == "Trend Analysis":
    st.title("Trend Analysis")

    crypto = st.selectbox("Select Cryptocurrency", df['cryptocurrency'].unique())
    crypto_df = df[df['cryptocurrency'] == crypto]

    fig = px.line(crypto_df, x='date', y='price', title=f"{crypto} Price Trend")
    st.plotly_chart(fig)

    fig2 = px.line(crypto_df, x='date', y='volume', title=f"{crypto} Volume Trend")
    st.plotly_chart(fig2)

    fig3 = px.line(df, x='date', y='price', color='cryptocurrency',
                   title="Multi Crypto Comparison")
    st.plotly_chart(fig3)

# ================= PRICE PREDICTION =================
# elif page == "Price Prediction":
#     st.title("Bitcoin Price Prediction")

#     model = joblib.load("model/model.pkl")

#     btc = df[df['cryptocurrency'] == 'Bitcoin'].copy()
#     btc = btc.sort_values('date')

#     # Create numeric feature
#     btc['days'] = (btc['date'] - btc['date'].min()).dt.days

#     # Prepare next day input WITH column name
#     next_day_value = btc['days'].max() + 1
#     next_day_df = pd.DataFrame([[next_day_value]], columns=['days'])

#     prediction = model.predict(next_day_df)

#     if st.button("Predict Next Day Price"):
#         st.markdown(f"""
#         <div style="
#             padding:30px;
#             border-radius:18px;
#             background:linear-gradient(135deg, rgba(34,197,94,0.15), rgba(59,130,246,0.15));
#             border:1px solid rgba(34,197,94,0.4);
#             text-align:center;
#         ">
#             <h2>Predicted Bitcoin Price</h2>
#             <h1 style="font-size:50px; color:#16a34a;">
#             ${prediction[0]:,.2f}
#             </h1>
#         </div>
#         """, unsafe_allow_html=True)

elif page == "Price Prediction":
    st.title("Bitcoin Price Prediction")

    model = joblib.load("model/model.pkl")

    btc = df[df['cryptocurrency'] == 'Bitcoin'].copy()
    btc = btc.sort_values('date')

    # Create numeric feature
    btc['days'] = (btc['date'] - btc['date'].min()).dt.days

    if st.button("Predict Next Day Price"):
        # Prepare next day input
        next_day_value = btc['days'].max() + 1
        next_day_df = pd.DataFrame([[next_day_value]], columns=['days'])

        prediction = model.predict(next_day_df)

        st.markdown(f"""
        <div style="
            padding:30px;
            border-radius:18px;
            background:linear-gradient(135deg, rgba(34,197,94,0.15), rgba(59,130,246,0.15));
            border:1px solid rgba(34,197,94,0.4);
            text-align:center;
        ">
            <h2>Predicted Bitcoin Price</h2>
            <h1 style="font-size:50px; color:#16a34a;">
            ${prediction[0]:,.2f}
            </h1>
        </div>
        """, unsafe_allow_html=True)

