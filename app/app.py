import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NCR Real Estate Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# HTML HELPER
# =========================================================

def render_html(html):
    """
    Render HTML safely using Streamlit's HTML renderer.
    textwrap.dedent removes unwanted indentation.
    """
    st.html(textwrap.dedent(html))


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* ================= HERO ================= */

    .hero {
        padding: 28px 32px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #172554,
            #1e3a8a,
            #312e81
        );
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin: 0 0 8px 0;
    }

    .hero p {
        color: #dbeafe;
        font-size: 18px;
        margin: 0;
    }

    /* ================= SECTION TITLE ================= */

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 28px;
        margin-bottom: 15px;
    }

    /* ================= KPI ================= */

    .kpi-card {
        background: linear-gradient(
            145deg,
            #171b24,
            #11141b
        );
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #292f3a;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.20);
        min-height: 115px;
    }

    .kpi-title {
        color: #9ca3af;
        font-size: 14px;
        letter-spacing: 0.5px;
        font-weight: 600;
    }

    .kpi-value {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin-top: 10px;
    }

    /* ================= INSIGHT ================= */

    .insight-card {
        background: linear-gradient(
            145deg,
            #172033,
            #111827
        );
        border-left: 4px solid #60a5fa;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.18);
    }

    .insight-title {
        color: #93c5fd;
        font-weight: 600;
        font-size: 16px;
    }

    .insight-text {
        color: #e5e7eb;
        font-size: 15px;
        margin-top: 6px;
        line-height: 1.5;
    }

    /* ================= FOOTER ================= */

    .footer {
        text-align: center;
        color: #9ca3af;
        padding: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/gurugram_real_estate_cleaned (1).csv"
    )

    # 999 means unknown BHK
    if "BHK_Count" in df.columns:
        df["BHK_Count"] = df["BHK_Count"].replace(
            999,
            pd.NA
        )

    # Convert numeric columns
    numeric_columns = [
        "Price",
        "Area",
        "Rate_per_sqft",
        "Calculated_Rate_per_sqft",
        "Price_Lakh",
        "BHK_Count"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


df = load_data()


# =========================================================
# HERO SECTION
# =========================================================

render_html(
    """
    <div class="hero">

        <h1>🏠 NCR Real Estate Market Analysis</h1>

        <p>
            Interactive Business Analytics Dashboard for the
            Gurugram Real Estate Market
        </p>

    </div>
    """
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore the real estate market."
)


# =========================================================
# PROPERTY TYPE FILTER
# =========================================================

property_types = sorted(
    df["Flat_Type"]
    .dropna()
    .astype(str)
    .unique()
)

selected_property_type = st.sidebar.multiselect(
    "🏢 Property Type",
    property_types,
    default=property_types
)


# =========================================================
# STATUS FILTER
# =========================================================

statuses = sorted(
    df["Status"]
    .dropna()
    .astype(str)
    .unique()
)

selected_status = st.sidebar.multiselect(
    "🏗️ Property Status",
    statuses,
    default=statuses
)


# =========================================================
# RERA FILTER
# =========================================================

rera_options = sorted(
    df["RERA_Approval"]
    .dropna()
    .astype(str)
    .unique()
)

selected_rera = st.sidebar.multiselect(
    "✅ RERA Approval",
    rera_options,
    default=rera_options
)


# =========================================================
# BHK FILTER
# =========================================================

bhk_values = sorted(
    df["BHK_Count"]
    .dropna()
    .unique()
)

selected_bhk = st.sidebar.multiselect(
    "🛏️ BHK",
    bhk_values,
    default=bhk_values
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df["Flat_Type"].isin(selected_property_type))
    &
    (df["Status"].isin(selected_status))
    &
    (df["RERA_Approval"].isin(selected_rera))
].copy()


if selected_bhk:

    filtered_df = filtered_df[
        filtered_df["BHK_Count"].isin(selected_bhk)
    ].copy()


# =========================================================
# EMPTY FILTER CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No properties match the selected filters. "
        "Please change your filter selection."
    )

    st.stop()


# =========================================================
# KPI SECTION
# =========================================================

st.markdown(
    '<div class="section-title">📊 Market Overview</div>',
    unsafe_allow_html=True
)


total_properties = len(filtered_df)

avg_price = filtered_df["Price_Lakh"].mean()

avg_rate = filtered_df["Rate_per_sqft"].mean()

avg_area = filtered_df["Area"].mean()


col1, col2, col3, col4 = st.columns(4)


# =========================================================
# KPI 1
# =========================================================

with col1:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                TOTAL PROPERTIES
            </div>

            <div class="kpi-value">
                {total_properties:,}
            </div>

        </div>
        """
    )


# =========================================================
# KPI 2
# =========================================================

with col2:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                AVERAGE PRICE
            </div>

            <div class="kpi-value">
                ₹{avg_price:,.2f} L
            </div>

        </div>
        """
    )


# =========================================================
# KPI 3
# =========================================================

with col3:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                AVG RATE / SQ.FT
            </div>

            <div class="kpi-value">
                ₹{avg_rate:,.0f}
            </div>

        </div>
        """
    )


# =========================================================
# KPI 4
# =========================================================

with col4:

    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                AVERAGE AREA
            </div>

            <div class="kpi-value">
                {avg_area:,.0f} sq.ft
            </div>

        </div>
        """
    )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Business Insights</div>',
    unsafe_allow_html=True
)


# =========================================================
# INSIGHT CALCULATIONS
# =========================================================

top_locality = (
    filtered_df["Locality"]
    .dropna()
    .value_counts()
    .idxmax()
)


top_locality_count = (
    filtered_df["Locality"]
    .dropna()
    .value_counts()
    .max()
)


common_property = (
    filtered_df["Flat_Type"]
    .dropna()
    .value_counts()
    .idxmax()
)


common_status = (
    filtered_df["Status"]
    .dropna()
    .value_counts()
    .idxmax()
)


if filtered_df["BHK_Count"].notna().any():

    common_bhk = (
        filtered_df["BHK_Count"]
        .dropna()
        .value_counts()
        .idxmax()
    )

else:

    common_bhk = "N/A"


rera_approved = (
    filtered_df["RERA_Approval"]
    .eq("Approved by RERA")
    .mean()
    * 100
)


# =========================================================
# BUSINESS INSIGHT CARDS
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# LEFT COLUMN
# =========================================================

with col1:

    render_html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                📍 Highest Listing Locality
            </div>

            <div class="insight-text">
                <b>{top_locality}</b> has the highest number
                of listings with
                <b>{top_locality_count:,}</b> properties.
            </div>

        </div>
        """
    )


    render_html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                🏢 Most Common Property Type
            </div>

            <div class="insight-text">
                <b>{common_property}</b> is the most frequently
                listed property type.
            </div>

        </div>
        """
    )


    render_html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                🏗️ Dominant Property Status
            </div>

            <div class="insight-text">
                <b>{common_status}</b> represents the largest
                share of properties.
            </div>

        </div>
        """
    )


# =========================================================
# RIGHT COLUMN
# =========================================================

with col2:

    render_html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                🛏️ Most Common BHK
            </div>

            <div class="insight-text">
                <b>{common_bhk} BHK</b> is the most frequently
                listed BHK configuration.
            </div>

        </div>
        """
    )


    render_html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                ✅ RERA Approved Properties
            </div>

            <div class="insight-text">
                Approximately <b>{rera_approved:.2f}%</b>
                of filtered properties are approved by RERA.
            </div>

        </div>
        """
    )


    render_html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                💰 Average Property Value
            </div>

            <div class="insight-text">
                The filtered market has an average property
                price of <b>₹{avg_price:,.2f} Lakh</b>.
            </div>

        </div>
        """
    )


# =========================================================
# PROPERTY TYPE ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">🏢 Property Type Analysis</div>',
    unsafe_allow_html=True
)


property_type_count = (
    filtered_df["Flat_Type"]
    .dropna()
    .value_counts()
    .reset_index()
)


property_type_count.columns = [
    "Property_Type",
    "Count"
]


fig_property = px.bar(
    property_type_count,
    x="Count",
    y="Property_Type",
    orientation="h",
    text="Count",
    title="Property Type Distribution"
)


fig_property.update_traces(
    textposition="outside"
)


fig_property.update_layout(
    template="plotly_dark",
    height=450,
    xaxis_title="Number of Listings",
    yaxis_title="Property Type"
)


st.plotly_chart(
    fig_property,
    width="stretch"
)


# =========================================================
# LOCALITY ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">📍 Locality Analysis</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# =========================================================
# TOP LOCALITIES BY LISTINGS
# =========================================================

with col1:

    top_localities = (
        filtered_df["Locality"]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )


    top_localities.columns = [
        "Locality",
        "Listings"
    ]


    fig1 = px.bar(
        top_localities,
        x="Listings",
        y="Locality",
        orientation="h",
        text="Listings",
        title="Top 10 Localities by Listings"
    )


    fig1.update_traces(
        textposition="outside"
    )


    fig1.update_layout(
        template="plotly_dark",
        height=500
    )


    st.plotly_chart(
        fig1,
        width="stretch"
    )


# =========================================================
# TOP LOCALITIES BY AVERAGE PRICE
# =========================================================

with col2:

    locality_price = (
        filtered_df
        .dropna(subset=["Locality"])
        .groupby("Locality")["Price_Lakh"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )


    fig2 = px.bar(
        locality_price,
        x="Price_Lakh",
        y="Locality",
        orientation="h",
        text="Price_Lakh",
        title="Top 10 Localities by Average Price"
    )


    fig2.update_traces(
        texttemplate="₹%{text:.0f} L",
        textposition="outside"
    )


    fig2.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Average Price (Lakh)"
    )


    st.plotly_chart(
        fig2,
        width="stretch"
    )


# =========================================================
# BHK ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">🛏️ BHK Price Analysis</div>',
    unsafe_allow_html=True
)


bhk_avg = (
    filtered_df
    .dropna(subset=["BHK_Count"])
    .groupby("BHK_Count")["Price_Lakh"]
    .mean()
    .sort_index()
    .reset_index()
)


# Keep common residential configurations
bhk_avg = bhk_avg[
    bhk_avg["BHK_Count"] <= 5
]


if not bhk_avg.empty:

    fig_bhk = px.bar(
        bhk_avg,
        x="BHK_Count",
        y="Price_Lakh",
        text="Price_Lakh",
        title="Average Residential Property Price by BHK"
    )


    fig_bhk.update_traces(
        texttemplate="₹%{text:.0f} L",
        textposition="outside"
    )


    fig_bhk.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="BHK",
        yaxis_title="Average Price (Lakh)"
    )


    st.plotly_chart(
        fig_bhk,
        width="stretch"
    )


# =========================================================
# AREA VS PRICE
# =========================================================

st.markdown(
    '<div class="section-title">📐 Area vs Price</div>',
    unsafe_allow_html=True
)


# Remove extreme outliers only from visualization
area_price_plot = filtered_df[
    (filtered_df["Area"] <= filtered_df["Area"].quantile(0.99))
    &
    (filtered_df["Price_Lakh"] <= filtered_df["Price_Lakh"].quantile(0.99))
].copy()


fig_area = px.scatter(
    area_price_plot,
    x="Area",
    y="Price_Lakh",
    color="Flat_Type",
    hover_data=[
        "Locality",
        "BHK_Count",
        "Status"
    ],
    title="Property Area vs Price"
)


fig_area.update_layout(
    template="plotly_dark",
    height=550,
    xaxis_title="Area (sq.ft)",
    yaxis_title="Price (Lakh)"
)


st.plotly_chart(
    fig_area,
    width="stretch"
)


# =========================================================
# RATE PER SQ.FT ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">💰 Rate per Sq.ft Analysis</div>',
    unsafe_allow_html=True
)


locality_rate = (
    filtered_df
    .dropna(subset=["Locality"])
    .groupby("Locality")["Rate_per_sqft"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)


fig_rate = px.bar(
    locality_rate,
    x="Rate_per_sqft",
    y="Locality",
    orientation="h",
    text="Rate_per_sqft",
    title="Top 10 Localities by Average Rate per Sq.ft"
)


fig_rate.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside"
)


fig_rate.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Average Rate (₹/sq.ft)"
)


st.plotly_chart(
    fig_rate,
    width="stretch"
)


# =========================================================
# PROPERTY STATUS + RERA
# =========================================================

st.markdown(
    '<div class="section-title">🏗️ Property Status & RERA</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# =========================================================
# PROPERTY STATUS
# =========================================================

with col1:

    status_count = (
        filtered_df["Status"]
        .dropna()
        .value_counts()
        .reset_index()
    )


    status_count.columns = [
        "Status",
        "Count"
    ]


    fig_status = px.pie(
        status_count,
        names="Status",
        values="Count",
        hole=0.45,
        title="Property Status Distribution"
    )


    fig_status.update_layout(
        template="plotly_dark",
        height=450
    )


    st.plotly_chart(
        fig_status,
        width="stretch"
    )


# =========================================================
# RERA DISTRIBUTION
# =========================================================

with col2:

    rera_count = (
        filtered_df["RERA_Approval"]
        .dropna()
        .value_counts()
        .reset_index()
    )


    rera_count.columns = [
        "RERA_Status",
        "Count"
    ]


    fig_rera = px.bar(
        rera_count,
        x="RERA_Status",
        y="Count",
        text="Count",
        title="RERA Approval Distribution"
    )


    fig_rera.update_traces(
        textposition="outside"
    )


    fig_rera.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="RERA Status",
        yaxis_title="Number of Listings"
    )


    st.plotly_chart(
        fig_rera,
        width="stretch"
    )


# =========================================================
# BUILDER / LISTING SOURCE ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">🏢 Builder / Listing Source Analysis</div>',
    unsafe_allow_html=True
)


st.caption(
    "Note: Builder_Name contains both builder names and listing-source/agent "
    "entries, so this chart should be interpreted as listing-source activity "
    "rather than a pure builder market-share analysis."
)


builder_count = (
    filtered_df["Builder_Name"]
    .dropna()
    .astype(str)
    .value_counts()
    .head(10)
    .reset_index()
)


builder_count.columns = [
    "Builder",
    "Listings"
]


fig_builder = px.bar(
    builder_count,
    x="Listings",
    y="Builder",
    orientation="h",
    text="Listings",
    title="Top 10 Builder / Listing Sources by Listings"
)


fig_builder.update_traces(
    textposition="outside"
)


fig_builder.update_layout(
    template="plotly_dark",
    height=500
)


st.plotly_chart(
    fig_builder,
    width="stretch"
)


# =========================================================
# RERA VS PRICE
# =========================================================

st.markdown(
    '<div class="section-title">💵 RERA vs Property Price</div>',
    unsafe_allow_html=True
)


rera_price = (
    filtered_df
    .dropna(subset=["RERA_Approval"])
    .groupby("RERA_Approval")["Price_Lakh"]
    .mean()
    .reset_index()
)


fig_rera_price = px.bar(
    rera_price,
    x="RERA_Approval",
    y="Price_Lakh",
    text="Price_Lakh",
    title="Average Property Price by RERA Approval"
)


fig_rera_price.update_traces(
    texttemplate="₹%{text:.0f} L",
    textposition="outside"
)


fig_rera_price.update_layout(
    template="plotly_dark",
    height=450,
    xaxis_title="RERA Approval",
    yaxis_title="Average Price (Lakh)"
)


st.plotly_chart(
    fig_rera_price,
    width="stretch"
)


# =========================================================
# CORRELATION
# =========================================================

st.markdown(
    '<div class="section-title">📈 Price Correlation</div>',
    unsafe_allow_html=True
)


correlation = filtered_df[
    ["Area", "Price_Lakh"]
].corr()


fig_corr = px.imshow(
    correlation,
    text_auto=".2f",
    title="Area vs Price Correlation",
    color_continuous_scale="Blues"
)


fig_corr.update_layout(
    template="plotly_dark",
    height=400
)


st.plotly_chart(
    fig_corr,
    width="stretch"
)


# =========================================================
# DATA TABLE
# =========================================================

st.markdown(
    '<div class="section-title">📋 Property Data</div>',
    unsafe_allow_html=True
)


st.write(
    f"Showing **{len(filtered_df):,}** properties "
    "based on selected filters."
)


display_columns = [
    "Price_Lakh",
    "Area",
    "Rate_per_sqft",
    "Property_Type",
    "Locality",
    "BHK_Count",
    "Flat_Type",
    "Status",
    "RERA_Approval"
]


display_columns = [
    col
    for col in display_columns
    if col in filtered_df.columns
]


st.dataframe(
    filtered_df[display_columns].head(100),
    width="stretch",
    height=500
)


# =========================================================
# FOOTER
# =========================================================

st.divider()


render_html(
    """
    <div class="footer">

        🏠 <b>NCR Real Estate Market Analysis</b>
        <br>

        Built with Python • Pandas • Plotly • Streamlit

    </div>
    """
)