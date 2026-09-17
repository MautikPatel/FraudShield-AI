"""
FraudShield AI
Executive Fraud Monitoring Dashboard
"""

import requests
import pandas as pd
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide",
)


# --------------------------------------------------
# API HELPERS
# --------------------------------------------------

def get_api_data(endpoint: str):
    """Fetch data from the FraudShield API."""

    response = requests.get(
        f"{API_BASE_URL}{endpoint}",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("FraudShield AI")

st.caption(
    "Real-Time Payment Fraud Detection & Risk Monitoring"
)

st.divider()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    stats = get_api_data(
        "/transactions/stats"
    )

    risk_distribution = get_api_data(
        "/transactions/analytics/risk-distribution"
    )

    countries = get_api_data(
        "/transactions/analytics/countries"
    )

    merchant_categories = get_api_data(
        "/transactions/analytics/merchant-categories"
    )

    high_risk_transactions = get_api_data(
        "/transactions/analytics/high-risk"
    )

except requests.RequestException as error:

    st.error(
        "Unable to connect to FraudShield API."
    )

    st.code(str(error))

    st.stop()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("Fraud Monitoring Overview")


col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric(
        "Transactions",
        f"{stats['total_transactions']:,}",
    )


with col2:
    st.metric(
        "Blocked",
        f"{stats['blocked_transactions']:,}",
    )


with col3:
    st.metric(
        "Review",
        f"{stats['review_transactions']:,}",
    )


with col4:
    st.metric(
        "Approved",
        f"{stats['approved_transactions']:,}",
    )


with col5:
    st.metric(
        "Block Rate",
        f"{stats['blocked_rate']:.2f}%",
    )


st.divider()


# --------------------------------------------------
# RISK OVERVIEW
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("Transaction Decisions")

    decision_df = pd.DataFrame(
        {
            "Status": list(
                risk_distribution.keys()
            ),
            "Transactions": list(
                risk_distribution.values()
            ),
        }
    )

    decision_df = decision_df.set_index(
        "Status"
    )

    st.bar_chart(
        decision_df
    )


with col2:

    st.subheader("Risk by Country")

    country_df = pd.DataFrame(
        countries
    )

    if not country_df.empty:

        country_chart = country_df[
            [
                "country",
                "average_risk",
            ]
        ].set_index(
            "country"
        )

        st.bar_chart(
            country_chart
        )


st.divider()

# --------------------------------------------------
# MERCHANT RISK
# --------------------------------------------------

st.subheader(
    "Merchant Category Risk"
)

merchant_df = pd.DataFrame(
    merchant_categories
)

if not merchant_df.empty:

    merchant_chart = (
        merchant_df[
            [
                "merchant_category",
                "average_risk",
            ]
        ]
        .sort_values(
            "average_risk",
            ascending=False,
        )
        .set_index(
            "merchant_category"
        )
    )

    st.bar_chart(
        merchant_chart,
        horizontal=True,
        x_label="Average Risk Score",
        y_label="Merchant Category",
    )


# --------------------------------------------------
# HIGH-RISK TRANSACTIONS
# --------------------------------------------------

st.subheader(
    "High-Risk Transactions"
)

high_risk_df = pd.DataFrame(
    high_risk_transactions
)

if not high_risk_df.empty:

    display_columns = [
        "transaction_id",
        "merchant_name",
        "merchant_category",
        "amount",
        "currency",
        "country",
        "risk_score",
        "fraud_status",
        "transaction_time",
    ]

    display_df = high_risk_df[
        display_columns
    ].copy()

    display_df["amount"] = (
        display_df["amount"]
        .round(2)
    )

    display_df["risk_score"] = (
        display_df["risk_score"]
        .round(2)
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No high-risk transactions found."
    )


st.divider()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption(
    "FraudShield AI | Hybrid Rule + ML Fraud Decisioning"
)