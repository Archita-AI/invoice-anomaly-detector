import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="Invoice Anomaly Detector",
    page_icon="🔍",
    layout="wide"
)


# =========================================
# DATA INPUT
# =========================================

st.sidebar.header("📁 Data Input")

uploaded_file = st.sidebar.file_uploader(
    "Upload Invoice CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.sidebar.success(
        "Invoice file uploaded successfully!"
    )

else:

    df = pd.read_csv(
        "data/final_invoices.csv"
    )

    st.sidebar.info(
        "Using project dataset."
    )


# =========================================
# SIDEBAR FILTERS
# =========================================

st.sidebar.header("🔎 Filters")


selected_vendors = st.sidebar.multiselect(
    "Select Vendor",
    options=sorted(df["vendor"].unique()),
    default=sorted(df["vendor"].unique())
)


selected_risk = st.sidebar.multiselect(
    "Risk Level",
    options=["Low", "Medium", "High"],
    default=["Low", "Medium", "High"]
)


selected_result = st.sidebar.multiselect(
    "Model Result",
    options=["Normal", "Anomaly"],
    default=["Normal", "Anomaly"]
)


# =========================================
# APPLY FILTERS
# =========================================

filtered_df = df[
    (df["vendor"].isin(selected_vendors)) &
    (df["risk_level"].isin(selected_risk)) &
    (df["model_result"].isin(selected_result))
]


# =========================================
# TITLE
# =========================================

st.title("🔍 Invoice Anomaly Detector")

st.write(
    "Machine learning-based system for identifying "
    "unusual invoice transactions for human review."
)

st.divider()


# =========================================
# KEY STATISTICS
# =========================================

total_invoices = len(filtered_df)

anomalies = (
    filtered_df["model_result"] == "Anomaly"
).sum()

normal = (
    filtered_df["model_result"] == "Normal"
).sum()

high_risk = (
    filtered_df["risk_level"] == "High"
).sum()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Invoices",
        total_invoices
    )


with col2:

    st.metric(
        "Anomalies",
        anomalies
    )


with col3:

    st.metric(
        "Normal Invoices",
        normal
    )


with col4:

    st.metric(
        "High Risk",
        high_risk
    )


st.divider()


# =========================================
# CHARTS
# =========================================

col1, col2 = st.columns(2)


# -----------------------------------------
# RISK DISTRIBUTION
# -----------------------------------------

with col1:

    risk_counts = (
        filtered_df["risk_level"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk Level",
        "Count"
    ]

    fig = px.pie(
        risk_counts,
        names="Risk Level",
        values="Count",
        title="Risk Level Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------------------------
# ANOMALIES BY VENDOR
# -----------------------------------------

with col2:

    vendor_anomalies = (
        filtered_df[
            filtered_df["model_result"] == "Anomaly"
        ]
        ["vendor"]
        .value_counts()
        .reset_index()
    )

    vendor_anomalies.columns = [
        "Vendor",
        "Anomalies"
    ]

    fig = px.bar(
        vendor_anomalies,
        x="Vendor",
        y="Anomalies",
        title="Anomalies by Vendor"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()


# =========================================
# INVOICE AMOUNT DISTRIBUTION
# =========================================

st.subheader("📊 Invoice Amount Distribution")


fig = px.histogram(
    filtered_df,
    x="amount",
    color="model_result",
    title="Invoice Amount Distribution",
    nbins=40
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.divider()


# =========================================
# MOST SUSPICIOUS INVOICES
# =========================================

st.subheader("🚨 Most Suspicious Invoices")


suspicious = (
    filtered_df
    .sort_values(
        "risk_score",
        ascending=False
    )
    [
        [
            "invoice_id",
            "vendor",
            "amount",
            "risk_score",
            "risk_level",
            "model_result"
        ]
    ]
    .head(20)
)


st.dataframe(
    suspicious,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================
# INVOICE INVESTIGATION
# =========================================

st.subheader("🔎 Investigate an Invoice")


invoice_ids = filtered_df[
    "invoice_id"
].tolist()


if len(invoice_ids) > 0:

    selected_invoice = st.selectbox(
        "Select an invoice",
        invoice_ids
    )


    invoice = filtered_df[
        filtered_df["invoice_id"]
        == selected_invoice
    ].iloc[0]


    col1, col2, col3 = st.columns(3)


    # -------------------------------------
    # BASIC INFORMATION
    # -------------------------------------

    with col1:

        st.write("### Invoice")

        st.write(
            invoice["invoice_id"]
        )

        st.write("### Vendor")

        st.write(
            invoice["vendor"]
        )


    # -------------------------------------
    # AMOUNT AND RISK SCORE
    # -------------------------------------

    with col2:

        st.write("### Amount")

        st.write(
            f"₹{invoice['amount']:,.2f}"
        )

        st.write("### Risk Score")

        st.write(
            f"{invoice['risk_score']:.2f}"
        )


    # -------------------------------------
    # RISK INFORMATION
    # -------------------------------------

    with col3:

        st.write("### Risk Level")

        st.write(
            invoice["risk_level"]
        )

        st.write("### Model Result")

        st.write(
            invoice["model_result"]
        )


    # -------------------------------------
    # EXPLANATION
    # -------------------------------------

    st.write(
        "### Why was this invoice flagged?"
    )


    st.info(
        invoice["explanation"]
    )


    # -------------------------------------
    # DUPLICATE CHECK
    # -------------------------------------

    st.write(
        "### Duplicate Check"
    )


    if invoice["is_duplicate"]:

        st.warning(
            "Potential duplicate invoice detected."
        )

    else:

        st.success(
            "No duplicate characteristics detected."
        )


else:

    st.warning(
        "No invoices match the selected filters."
    )


st.divider()


# =========================================
# VENDOR ANALYSIS
# =========================================

st.subheader("🏢 Vendor Analysis")


vendor_summary = (
    filtered_df
    .groupby("vendor")
    .agg(
        invoices=(
            "invoice_id",
            "count"
        ),

        average_amount=(
            "amount",
            "mean"
        ),

        anomalies=(
            "model_result",
            lambda x: (
                x == "Anomaly"
            ).sum()
        ),

        high_risk=(
            "risk_level",
            lambda x: (
                x == "High"
            ).sum()
        )
    )
    .reset_index()
)


vendor_summary[
    "average_amount"
] = (
    vendor_summary[
        "average_amount"
    ].round(2)
)


st.dataframe(
    vendor_summary,
    use_container_width=True,
    hide_index=True
)


# =========================================
# FOOTER
# =========================================

st.divider()

st.caption(
    "Machine Learning-Based Invoice Anomaly Detector | "
    "Designed to identify unusual transactions for "
    "human review. An anomaly does not necessarily "
    "indicate fraud."
)