"""
FraudShield AI
Fraud Operations Dashboard

Read-only operational dashboard for the FraudShield API.
"""

import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE_URL = os.getenv(
    "FRAUDSHIELD_API_URL",
    "http://127.0.0.1:8000",
)

REQUEST_TIMEOUT = 10
CACHE_TTL_SECONDS = 15


st.set_page_config(
    page_title="FraudShield AI",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    },
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
        :root {
            --navy: #0b1f3a;
            --navy-2: #12345b;
            --blue: #2563eb;
            --blue-soft: #eaf2ff;
            --text: #172033;
            --muted: #6b7280;
            --border: #dfe5ec;
            --surface: #ffffff;
            --page: #f5f7fa;
            --danger: #c62828;
            --warning: #b26a00;
            --success: #237a4b;
        }

        .stApp {
            background: var(--page);
        }

        /* Global typography: increase native Streamlit text by 2px. */
        html, body, [class*="css"] {
            font-size: 18px;
        }

        /* Keep inputs as native browser controls so Ctrl+C/Ctrl+V
           and right-click paste work normally. */
        input,
        textarea,
        [contenteditable="true"] {
            font-size: 18px !important;
            user-select: text !important;
            -webkit-user-select: text !important;
            pointer-events: auto !important;
        }

        [data-testid="stTextInput"] input {
            font-size: 18px !important;
            padding: 0.55rem 0.75rem !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] {
            font-size: 18px !important;
        }

        [data-testid="stSlider"] {
            font-size: 18px !important;
        }

        [data-testid="stCaptionContainer"] {
            font-size: 16px !important;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1500px;
            padding-top: 1.25rem;
            padding-bottom: 2rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #081b34 0%,
                #0d2949 100%
            );
        }

        [data-testid="stSidebar"] * {
            color: #e7eef7;
        }

        .brand {
            font-size: 2.125rem;
            font-weight: 700;
            letter-spacing: 0.2px;
            margin-bottom: 0.15rem;
        }

        .brand-subtitle {
            color: #9fb3ca;
            font-size: 1.875rem;
            margin-bottom: 1.4rem;
        }

        .nav-label {
            color: #9fb3ca;
            font-size: 0.825rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 1.2rem;
            margin-bottom: 0.45rem;
        }

        .profile-box {
            border-top: 1px solid rgba(255,255,255,0.12);
            margin-top: 1.2rem;
            padding-top: 1rem;
        }

        .page-title {
            color: var(--text);
            font-size: 1.975rem;
            font-weight: 700;
            line-height: 1.15;
            margin-bottom: 0.15rem;
        }

        .page-subtitle {
            color: var(--muted);
            font-size: 1.005rem;
            margin-bottom: 1rem;
        }

        .section-heading {
            color: var(--text);
            font-size: 1.175rem;
            font-weight: 650;
            margin: 0.15rem 0 0.7rem 0;
        }

        .detail-grid-title {
            color: var(--text);
            font-size: 1.125rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }

        .status-card {
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--surface);
            padding: 0.85rem 0.95rem;
            min-height: 102px;
        }

        .status-label {
            color: var(--muted);
            font-size: 0.885rem;
            margin-bottom: 0.25rem;
        }

        .status-value {
            color: var(--text);
            font-size: 1.375rem;
            font-weight: 700;
        }

        .status-detail {
            color: var(--muted);
            font-size: 0.845rem;
            margin-top: 0.2rem;
        }

        .model-box {
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--surface);
            padding: 1rem;
        }

        .model-title {
            font-weight: 650;
            color: var(--text);
            margin-bottom: 0.7rem;
        }

        .model-row {
            display: flex;
            justify-content: space-between;
            padding: 0.28rem 0;
            border-bottom: 1px solid #eef1f5;
            font-size: 0.925rem;
        }

        .model-row:last-child {
            border-bottom: none;
        }

        .model-key {
            color: var(--muted);
        }

        .model-value {
            color: var(--text);
            font-weight: 600;
        }

        .footer-note {
            color: #7b8491;
            font-size: 0.845rem;
            margin-top: 1.25rem;
        }

        div[data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.85rem 0.95rem;
        }

        div[data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        div[data-testid="stMetricValue"] {
            color: var(--text);
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
        }

        .small-note {
            color: var(--muted);
            font-size: 0.865rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API HELPERS
# ============================================================

def get_api_data(endpoint: str, params: dict | None = None):
    """Fetch JSON data from the FraudShield API."""

    response = requests.get(
        f"{API_BASE_URL}{endpoint}",
        params=params,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()

def get_transaction_detail(transaction_id: str,):
    """
    Return detailed transaction information,
    including fraud decision explanation.
    """

    return get_api_data(
        f"/transactions/{transaction_id}"
    )


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def load_dashboard_data():
    """Load all dashboard datasets with short-lived caching."""

    return {
        "stats": get_api_data("/transactions/stats"),
        "risk_distribution": get_api_data(
            "/transactions/analytics/risk-distribution"
        ),
        "countries": get_api_data(
            "/transactions/analytics/countries"
        ),
        "merchant_categories": get_api_data(
            "/transactions/analytics/merchant-categories"
        ),
        "high_risk": get_api_data(
            "/transactions/analytics/high-risk"
        ),
        "transactions": get_api_data(
            "/transactions/",
            params={"limit": 1000},
        ),
        "health": get_api_data("/health"),
    }


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">FraudShield AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-subtitle">'
        "Payment Fraud Operations"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="nav-label">Monitoring</div>',
        unsafe_allow_html=True,
    )
    
    navigation = st.radio(
    "Navigation",
    [
        "Dashboard",
        "Transactions",
        "Alerts",
    ],
    label_visibility="collapsed",
)

    if "page_override" not in st.session_state:
        st.session_state["page_override"] = None

    if st.session_state["page_override"]:
        navigation = st.session_state["page_override"]
        st.session_state["page_override"] = None

    st.markdown(
        '<div class="nav-label">Management</div>',
        unsafe_allow_html=True,
    )

    st.caption("Reports")
    st.caption("Settings")

    st.markdown(
        '<div class="profile-box">'
        "<strong>Fraud Operations</strong><br>"
        '<span style="color:#9fb3ca;font-size: 0.875rem;">'
        "Hybrid Rule + ML Decisioning"
        "</span>"
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD DATA
# ============================================================

try:
    data = load_dashboard_data()

except requests.RequestException as error:
    st.error("FraudShield API is unavailable.")

    st.write(
        "Start FastAPI and verify that the API is reachable at:"
    )

    st.code(API_BASE_URL)

    with st.expander("Technical details"):
        st.code(str(error))

    st.stop()


stats = data["stats"]
risk_distribution = data["risk_distribution"]
countries = data["countries"]
merchant_categories = data["merchant_categories"]
high_risk_transactions = data["high_risk"]
transactions = data["transactions"]


# ============================================================
# REFRESH
# ============================================================

refresh_col1, refresh_col2 = st.columns([8, 1])

with refresh_col2:
    if st.button("Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


last_updated = datetime.now().strftime(
    "%d %b %Y, %H:%M:%S"
)


# ============================================================
# DASHBOARD
# ============================================================

if navigation == "Dashboard":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="page-title">'
        "Dashboard Overview"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        "Real-time payment fraud detection and risk monitoring"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        f"Last updated: {last_updated}"
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    total = stats["total_transactions"]
    blocked = stats["blocked_transactions"]
    review = stats["review_transactions"]
    approved = stats["approved_transactions"]
    flagged = blocked + review
    block_rate = stats["blocked_rate"]
    avg_risk = stats["average_risk_score"]

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.metric(
            "Total Transactions",
            f"{total:,}",
        )

    with k2:
        st.metric(
            "Flagged Activity",
            f"{flagged:,}",
        )

    with k3:
        st.metric(
            "Blocked Transactions",
            f"{blocked:,}",
        )

    with k4:
        st.metric(
            "Average Risk",
            f"{avg_risk:.2f}",
        )

    with k5:
        st.metric(
            "Block Rate",
            f"{block_rate:.2f}%",
        )

    st.write("")

    # --------------------------------------------------------
    # RISK ACTIVITY + ENGINE STATUS
    # --------------------------------------------------------

    left, right = st.columns([2.2, 1])

    with left:
        st.markdown(
            '<div class="section-heading">'
            "Risk Decision Distribution"
            "</div>",
            unsafe_allow_html=True,
        )

        decision_df = pd.DataFrame(
            {
                "Decision": [
                    "Approved",
                    "Review",
                    "Blocked",
                ],
                "Transactions": [
                    risk_distribution.get("APPROVED", 0),
                    risk_distribution.get("REVIEW", 0),
                    risk_distribution.get("BLOCKED", 0),
                ],
            }
        )

        fig = px.bar(
            decision_df,
            x="Decision",
            y="Transactions",
            text="Transactions",
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "%{x}<br>"
                "Transactions: %{y:,}"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            height=500,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with right:
        st.markdown(
            '<div class="section-heading">'
            "Fraud Engine Status"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="status-card">
                <div class="status-label">Decision Engine</div>
                <div class="status-value">Active</div>
                <div class="status-detail">
                    FastAPI and database connected
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style=\"height:8px;\"></div>", unsafe_allow_html=True)

        # Native Streamlit layout is used here instead of multiline HTML.
        # This prevents Streamlit Markdown from interpreting the panel as a code block.
        with st.container(border=True):
            st.markdown("**Hybrid Risk Model**")

            model_col1, model_col2 = st.columns([2, 1])

            with model_col1:
                st.caption("Rule Engine")
                st.caption("ML Model")
                st.caption("Risk Score")
                st.caption("Review Threshold")
                st.caption("Block Threshold")
                st.caption("Hard Block Override")

            with model_col2:
                st.markdown("**40%**")
                st.markdown("**60%**")
                st.markdown("**0–100**")
                st.markdown("**40**")
                st.markdown("**80**")
                st.markdown("**Enabled**")

    # --------------------------------------------------------
    # COUNTRY + DECISION BREAKDOWN
    # --------------------------------------------------------

    left, right = st.columns([1.55, 1])

    with left:
        st.markdown(
            '<div class="section-heading">'
            "High-Risk Countries"
            "</div>",
            unsafe_allow_html=True,
        )

        country_df = pd.DataFrame(countries)

        if not country_df.empty:
            country_df = country_df.sort_values(
                "average_risk",
                ascending=True,
            ).tail(10)

            fig = px.bar(
                country_df,
                x="average_risk",
                y="country",
                orientation="h",
                text="average_risk",
            )

            fig.update_traces(
                texttemplate="%{text:.1f}",
                textposition="outside",
                hovertemplate=(
                    "%{y}<br>"
                    "Average Risk: %{x:.2f}<br>"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=340,
                margin=dict(
                    l=20,
                    r=50,
                    t=10,
                    b=20,
                ),
                xaxis_title="Average Risk Score",
                yaxis_title=None,
                xaxis=dict(
                    range=[
                        0,
                        max(
                            100,
                            float(
                                country_df["average_risk"].max()
                            ) * 1.15,
                        ),
                    ]
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:
            st.info("No country risk data available.")

    with right:
        st.markdown(
            '<div class="section-heading">'
            "Decision Breakdown"
            "</div>",
            unsafe_allow_html=True,
        )

        donut_df = pd.DataFrame(
            {
                "Decision": [
                    "Approved",
                    "Review",
                    "Blocked",
                ],
                "Count": [
                    risk_distribution.get("APPROVED", 0),
                    risk_distribution.get("REVIEW", 0),
                    risk_distribution.get("BLOCKED", 0),
                ],
            }
        )

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=donut_df["Decision"],
                    values=donut_df["Count"],
                    hole=0.62,
                    textinfo="percent",
                    hovertemplate=(
                        "%{label}<br>"
                        "Transactions: %{value:,}<br>"
                        "Share: %{percent}"
                        "<extra></extra>"
                    ),
                )
            ]
        )

        fig.update_layout(
            height=340,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10,
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                y=-0.05,
                x=0.5,
                xanchor="center",
            ),
            paper_bgcolor="white",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # MERCHANT CATEGORY RISK
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">'
        "Merchant Category Risk"
        "</div>",
        unsafe_allow_html=True,
    )

    merchant_df = pd.DataFrame(
        merchant_categories
    )

    if not merchant_df.empty:

        merchant_df = merchant_df.sort_values(
            "average_risk",
            ascending=True,
        )

        fig = px.bar(
            merchant_df,
            x="average_risk",
            y="merchant_category",
            orientation="h",
            text="average_risk",
        )

        fig.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside",
            hovertemplate=(
                "%{y}<br>"
                "Average Risk: %{x:.2f}<br>"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            height=420,
            margin=dict(
                l=20,
                r=55,
                t=10,
                b=20,
            ),
            xaxis_title="Average Risk Score",
            yaxis_title=None,
            xaxis=dict(
                range=[
                    0,
                    max(
                        100,
                        float(
                            merchant_df["average_risk"].max()
                        ) * 1.15,
                    ),
                ]
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # RECENT ALERTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">'
        "Recent High-Risk Alerts"
        "</div>",
        unsafe_allow_html=True,
    )

    alerts_df = pd.DataFrame(
        high_risk_transactions
    )

    if not alerts_df.empty:

        alerts_df = alerts_df.head(80).copy()

        alerts_display = alerts_df[
            [
                "transaction_id",
                "merchant_name",
                "merchant_category",
                "country",
                "amount",
                "risk_score",
                "fraud_status",
            ]
        ].copy()

        alerts_display.columns = [
            "Transaction ID",
            "Merchant",
            "Category",
            "Country",
            "Amount",
            "Risk Score",
            "Decision",
        ]

        alerts_display["Amount"] = alerts_display[
            "Amount"
        ].map(
            lambda value: f"${float(value):,.2f}"
        )

        alerts_display["Risk Score"] = alerts_display[
            "Risk Score"
        ].map(
            lambda value: f"{float(value):.0f}"
        )

        st.dataframe(
            alerts_display,
            use_container_width=True,
            hide_index=True,
            height=310,
        )

    else:
        st.info("No high-risk alerts found.")

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown(
        '<div class="footer-note">'
        "FraudShield AI | Synthetic transaction data | "
        "Hybrid Rule + ML fraud decisioning"
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# TRANSACTIONS
# ============================================================

elif navigation == "Transactions":

    st.markdown(
        '<div class="page-title">'
        "Transactions"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        "Review the latest payment transactions evaluated by the fraud engine"
        "</div>",
        unsafe_allow_html=True,
    )

    transaction_df = pd.DataFrame(transactions)

    if transaction_df.empty:
        st.info("No transactions available.")
        st.stop()

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    search_col, status_col, country_col, risk_col = st.columns(
        [2.2, 1, 1, 1]
    )

    with search_col:
        search_input = st.text_input(
            "Search",
            placeholder="Transaction ID or merchant",
            key="transaction_search",
            help="Paste a Transaction ID or merchant name here.",
        )

        search_text = search_input.strip().lower()

    with status_col:
        status_options = [
            "All",
            "APPROVED",
            "REVIEW",
            "BLOCKED",
        ]

        selected_status = st.selectbox(
            "Decision",
            status_options,
        )

    with country_col:
        countries_available = sorted(
            transaction_df["country"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_country = st.selectbox(
            "Country",
            ["All"] + countries_available,
        )

    with risk_col:
        min_risk = st.slider(
            "Minimum Risk",
            min_value=0,
            max_value=100,
            value=0,
        )

    # --------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------

    filtered_df = transaction_df.copy()

    if search_text:
        filtered_df = filtered_df[
            filtered_df["transaction_id"].astype(str).str.lower().str.contains(
                search_text,
                na=False,
            )
            | filtered_df["merchant_name"].astype(str).str.lower().str.contains(
                search_text,
                na=False,
            )
        ]

    if selected_status != "All":
        filtered_df = filtered_df[
            filtered_df["fraud_status"] == selected_status
        ]

    if selected_country != "All":
        filtered_df = filtered_df[
            filtered_df["country"] == selected_country
        ]

    filtered_df["risk_score"] = pd.to_numeric(
        filtered_df["risk_score"],
        errors="coerce",
    )

    filtered_df = filtered_df[
        filtered_df["risk_score"] >= min_risk
    ]

    # Highest risk first for operational review.
    filtered_df = filtered_df.sort_values(
        ["risk_score", "transaction_time"],
        ascending=[False, False],
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.metric(
            "Loaded",
            f"{len(transaction_df):,}",
        )

    with result_col2:
        st.metric(
            "Matching Filters",
            f"{len(filtered_df):,}",
        )

    with result_col3:
        st.metric(
            "Database Population",
            f"{stats['total_transactions']:,}",
        )

    st.caption(
        "The dashboard loads the latest 100 transactions for operational review. "
        "Database Population reflects the complete PostgreSQL transaction count."
    )

    # --------------------------------------------------------
    # TRANSACTION TABLE
    # --------------------------------------------------------

    display_columns = [
        "transaction_id",
        "merchant_name",
        "merchant_category",
        "amount",
        "currency",
        "country",
        "payment_method",
        "risk_score",
        "fraud_status",
        "transaction_time",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in filtered_df.columns
    ]

    display_df = filtered_df[available_columns].copy()

    rename_map = {
        "transaction_id": "Transaction ID",
        "merchant_name": "Merchant",
        "merchant_category": "Category",
        "amount": "Amount",
        "currency": "Currency",
        "country": "Country",
        "payment_method": "Payment Method",
        "risk_score": "Risk Score",
        "fraud_status": "Decision",
        "transaction_time": "Transaction Time",
    }

    display_df = display_df.rename(columns=rename_map)

    if "Amount" in display_df.columns:
        display_df["Amount"] = display_df["Amount"].map(
            lambda value: f"${float(value):,.2f}"
        )

    if "Risk Score" in display_df.columns:
        display_df["Risk Score"] = display_df["Risk Score"].map(
            lambda value: f"{float(value):.2f}"
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=520,
    )

    # --------------------------------------------------------
    # SELECTED TRANSACTION DETAIL
    # --------------------------------------------------------

    if not filtered_df.empty:

        st.markdown(
            '<div class="section-heading">'
            "Transaction Details"
            "</div>",
            unsafe_allow_html=True,
        )

        transaction_options = filtered_df["transaction_id"].astype(str).tolist()

        selected_transaction_id = st.selectbox(
            "Select transaction",
            transaction_options,
            label_visibility="collapsed",
        )

        selected_transaction = filtered_df[
            filtered_df["transaction_id"].astype(str)
            == selected_transaction_id
        ].iloc[0]


        selected_transaction_id = selected_transaction[
            "transaction_id"
        ]

        try:
            selected_detail = get_transaction_detail(
                selected_transaction_id
            )
        except Exception:
            selected_detail = None

        # ---------------------------------------------------------
        # Transaction Detail
        # ---------------------------------------------------------

        selected_transaction_id = selected_transaction[
            "transaction_id"
        ]

        try:
            selected_detail = get_transaction_detail(
                selected_transaction_id
            )
        except Exception:
            selected_detail = None


        detail1, detail2, detail3 = st.columns(3)

        with detail1:
            st.markdown(
                '<div class="detail-grid-title">Transaction</div>',
                unsafe_allow_html=True,
            )

            st.write(
                f"ID: `{selected_transaction['transaction_id']}`"
            )
            st.write(
                f"Merchant: {selected_transaction['merchant_name']}"
            )
            st.write(
                f"Category: {selected_transaction['merchant_category']}"
            )
            st.write(
                f"Amount: ${float(selected_transaction['amount']):,.2f}"
            )


        with detail2:
            st.markdown(
                '<div class="detail-grid-title">Payment Context</div>',
                unsafe_allow_html=True,
            )

            st.write(
                f"Country: {selected_transaction['country']}"
            )
            st.write(
                f"Payment Method: "
                f"{selected_transaction['payment_method']}"
            )
            st.write(
                f"Transaction Time: "
                f"{selected_transaction['transaction_time']}"
            )


        with detail3:
            st.markdown(
                '<div class="detail-grid-title">Risk Assessment</div>',
                unsafe_allow_html=True,
            )

            st.metric(
                "Risk Score",
                f"{float(selected_transaction['risk_score']):.2f}",
            )

            st.write(
                f"Decision: **{selected_transaction['fraud_status']}**"
            )

            if selected_detail:
                explanation = selected_detail.get(
                    "explanation",
                    {},
                )

                if explanation:
                    st.write(
                        f"Risk Level: "
                        f"**{explanation.get('risk_level', 'N/A')}**"
                    )


        # ---------------------------------------------------------
        # AI Decision Explanation
        # ---------------------------------------------------------

        if selected_detail:
            explanation = selected_detail.get(
                "explanation",
                {},
            )

            if explanation:
                st.markdown(
                    '<div class="detail-grid-title">'
                    'AI Decision Explanation'
                    '</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="detail-grid-title">'
                    f'{explanation.get("headline", "Fraud Risk Assessment")}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                st.write(
                    explanation.get(
                        "natural_language_insight",
                        explanation.get("summary", ""),
                    )
                )

                signal_col, basis_col = st.columns(2)

                with signal_col:
                    st.markdown("**Key Signals**")

                    key_signals = explanation.get(
                        "key_signals",
                        [],
                    )

                    if key_signals:
                        for signal in key_signals:
                            st.write(f"• {signal}")
                    else:
                        st.write(
                            "• No significant risk signals detected."
                        )

                with basis_col:
                    st.markdown("**Decision Basis**")

                    st.write(
                        explanation.get(
                            "decision_basis",
                            "Not available.",
                        )
                    )

                    st.markdown("**ML Signal**")

                    st.write(
                        explanation.get(
                            "ml_signal",
                            "Not available.",
                        )
                    )

                st.markdown("**Recommended Action**")

                st.write(
                    explanation.get(
                        "recommended_action",
                        "No action specified.",
                    )
                )

        else:
            st.info(
                "Transaction explanation is currently unavailable."
            )

    else:
        st.info("No transactions match the selected filters.")

    st.caption(
        "Risk score is the final hybrid Rule + ML decision score. "
        "Blocked is an operational decision, not confirmation of fraud."
    )


# ============================================================
# ALERTS
# ============================================================
# ============================================================
# ALERTS
# ============================================================

elif navigation == "Alerts":

    st.markdown(
        '<div class="page-title">'
        "Alerts"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        "High-risk transactions requiring monitoring or investigation"
        "</div>",
        unsafe_allow_html=True,
    )

    alerts_df = pd.DataFrame(
        high_risk_transactions
    )

    if alerts_df.empty:
        st.success(
            "No high-risk transactions are currently available."
        )
        st.stop()

    # --------------------------------------------------------
    # Alert Summary
    # --------------------------------------------------------

    blocked_alerts = (
        alerts_df["fraud_status"]
        .eq("BLOCKED")
        .sum()
    )

    review_alerts = (
        alerts_df["fraud_status"]
        .eq("REVIEW")
        .sum()
    )

    highest_risk = (
        alerts_df["risk_score"]
        .astype(float)
        .max()
    )

    a1, a2, a3, a4 = st.columns(4)

    with a1:
        st.metric(
            "Active Alerts",
            f"{len(alerts_df):,}",
        )

    with a2:
        st.metric(
            "Blocked",
            f"{blocked_alerts:,}",
        )

    with a3:
        st.metric(
            "Review Required",
            f"{review_alerts:,}",
        )

    with a4:
        st.metric(
            "Highest Risk Score",
            f"{highest_risk:.0f}",
        )

    st.write("")

    # --------------------------------------------------------
    # Alert Queue
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-heading">'
        "Active High-Risk Alerts"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Highest-risk transactions are shown first."
    )

    # Highest risk first
    alerts_df = alerts_df.sort_values(
        by=["risk_score", "transaction_time"],
        ascending=[False, False],
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Alert Cards
    # --------------------------------------------------------

    for index, alert in alerts_df.iterrows():

        risk_score = float(
            alert["risk_score"]
        )

        decision = alert[
            "fraud_status"
        ]

        merchant = alert[
            "merchant_name"
        ]

        category = alert[
            "merchant_category"
        ]

        amount = float(
            alert["amount"]
        )

        currency = alert[
            "currency"
        ]

        country = alert[
            "country"
        ]

        transaction_id = alert[
            "transaction_id"
        ]

        transaction_time = alert[
            "transaction_time"
        ]

        # Derive the primary rule signals from
        # the same fraud rules used by the engine.
        signals = []

        if amount >= 6000:
            signals.append(
                "Very High Amount"
            )
        elif amount >= 3000:
            signals.append(
                "High Amount"
            )

        if country in [
            "Russia",
            "North Korea",
            "Iran",
        ]:
            signals.append(
                "High Risk Country"
            )

        if category in [
            "Electronics",
            "Luxury",
        ]:
            signals.append(
                "High Risk Merchant"
            )

        try:
            transaction_hour = (
                pd.to_datetime(
                    transaction_time
                ).hour
            )

            if (
                transaction_hour >= 23
                or transaction_hour < 5
            ):
                signals.append(
                    "Night Transaction"
                )

        except Exception:
            pass

        signal_text = (
            " • ".join(signals)
            if signals
            else "Elevated hybrid risk score"
        )

        with st.container(
            border=True
        ):

            alert_col1, alert_col2 = st.columns(
                [5, 1]
            )

            with alert_col1:

                st.markdown(
                    f"**{decision}**  "
                    f"Risk Score: **{risk_score:.0f}**"
                )

                st.markdown(
                    f"**{merchant}**"
                )

                st.caption(
                    f"{category} • "
                    f"{currency} "
                    f"{amount:,.2f} • "
                    f"{country}"
                )

                st.markdown(
                    f"**Risk Signals:** "
                    f"{signal_text}"
                )

                st.caption(
                    f"Transaction ID: "
                    f"`{transaction_id}` • "
                    f"{transaction_time}"
                )

            with alert_col2:

                st.write("")

                if st.button(
                    "View Transaction",
                    key=f"alert_{transaction_id}",
                    use_container_width=True,
                ):

                    st.session_state[
                        "selected_transaction_id"
                    ] = transaction_id

                    st.session_state[
                        "page_override"
                    ] = "Transactions"

                    st.rerun()
                    
    st.write("")

    st.caption(
        "Risk score is the final hybrid Rule + ML decision score. "
        "Blocked is an operational decision, not confirmation of fraud."
    )