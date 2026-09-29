import streamlit as st
import pandas as pd
import plotly.express as px


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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 25px 30px;
    border-radius: 18px;
    background: linear-gradient(135deg, #172554, #1e3a8a, #312e81);
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 42px;
    margin-bottom: 5px;
}

.hero p {
    color: #dbeafe;
    font-size: 18px;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

.kpi-card {
    background: linear-gradient(145deg, #171b24, #11141b);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #292f3a;
    text-align: center;
}

.kpi-title {
    color: #9ca3af;
    font-size: 14px;
}

.kpi-value {
    color: white;
    font-size: 28px;
    font-weight: 700;
    margin-top: 8px;
}

.insight-card {
    background: linear-gradient(145deg, #172033, #111827);
    border-left: 4px solid #60a5fa;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.insight-title {
    color: #93c5fd;
    font-weight: 600;
}

.insight-text {
    color: #e5e7eb;
    font-size: 15px;
    margin-top: 5px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/gurugram_real_estate_cleaned (1).csv"
    )

    # 999 = unknown BHK
    df["BHK_Count"] = df["BHK_Count"].replace(
        999,
        pd.NA
    )

    return df


df = load_data()


# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">

<h1>🏠 NCR Real Estate Market Analysis</h1>

<p>
Interactive Business Analytics Dashboard for the
Gurugram Real Estate Market
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore the real estate market."
)


# Property Type
property_types = sorted(
    df["Flat_Type"].dropna().unique()
)

selected_property_type = st.sidebar.multiselect(
    "🏢 Property Type",
    property_types,
    default=property_types
)


# Status
statuses = sorted(
    df["Status"].dropna().unique()
)

selected_status = st.sidebar.multiselect(
    "🏗️ Property Status",
    statuses,
    default=statuses
)


# RERA
rera_options = sorted(
    df["RERA_Approval"].dropna().unique()
)

selected_rera = st.sidebar.multiselect(
    "✅ RERA Approval",
    rera_options,
    default=rera_options
)


# BHK
bhk_values = sorted(
    df["BHK_Count"].dropna().unique()
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
    (df["Flat_Type"].isin(selected_property_type)) &
    (df["Status"].isin(selected_status)) &
    (df["RERA_Approval"].isin(selected_rera))
]

if selected_bhk:
    filtered_df = filtered_df[
        filtered_df["BHK_Count"].isin(selected_bhk)
    ]


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


with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">TOTAL PROPERTIES</div>
            <div class="kpi-value">{total_properties:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">AVERAGE PRICE</div>
            <div class="kpi-value">₹{avg_price:,.2f} L</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">AVG RATE / SQ.FT</div>
            <div class="kpi-value">₹{avg_rate:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">AVERAGE AREA</div>
            <div class="kpi-value">{avg_area:,.0f} sq.ft</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Business Insights</div>',
    unsafe_allow_html=True
)


if len(filtered_df) > 0:

    # Most listed locality
    top_locality = (
        filtered_df["Locality"]
        .value_counts()
        .idxmax()
    )

    top_locality_count = (
        filtered_df["Locality"]
        .value_counts()
        .max()
    )


    # Most common property type
    common_property = (
        filtered_df["Flat_Type"]
        .value_counts()
        .idxmax()
    )


    # Most common status
    common_status = (
        filtered_df["Status"]
        .value_counts()
        .idxmax()
    )


    # Most common BHK
    if filtered_df["BHK_Count"].notna().any():

        common_bhk = (
            filtered_df["BHK_Count"]
            .dropna()
            .value_counts()
            .idxmax()
        )

    else:

        common_bhk = "N/A"


    # RERA approved percentage
    rera_approved = (
        filtered_df["RERA_Approval"]
        == "Approved by RERA"
    ).mean() * 100


    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    📍 Highest Listing Locality
                </div>

                <div class="insight-text">
                    <b>{top_locality}</b> has the highest number
                    of listings with <b>{top_locality_count:,}</b>
                    properties.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
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
            """,
            unsafe_allow_html=True
        )


        st.markdown(
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
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
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
            """,
            unsafe_allow_html=True
        )


        st.markdown(
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
            """,
            unsafe_allow_html=True
        )


        st.markdown(
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
            """,
            unsafe_allow_html=True
        )


# =========================================================
# PROPERTY TYPE
# =========================================================

st.markdown(
    '<div class="section-title">🏢 Property Type Analysis</div>',
    unsafe_allow_html=True
)


property_type_count = (
    filtered_df["Flat_Type"]
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
    height=450
)

st.plotly_chart(
    fig_property,
    use_container_width=True
)


# =========================================================
# LOCALITY ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">📍 Locality Analysis</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# Top Localities
with col1:

    top_localities = (
        filtered_df["Locality"]
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

    fig1.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )


# Average Locality Price
with col2:

    locality_price = (
        filtered_df
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

    fig2.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
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

bhk_avg = bhk_avg[
    bhk_avg["BHK_Count"] <= 5
]


fig_bhk = px.bar(
    bhk_avg,
    x="BHK_Count",
    y="Price_Lakh",
    text="Price_Lakh",
    title="Average Residential Property Price by BHK"
)

fig_bhk.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(
    fig_bhk,
    use_container_width=True
)


# =========================================================
# AREA VS PRICE
# =========================================================

st.markdown(
    '<div class="section-title">📐 Area vs Price</div>',
    unsafe_allow_html=True
)


fig_area = px.scatter(
    filtered_df,
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
    height=550
)

st.plotly_chart(
    fig_area,
    use_container_width=True
)


# =========================================================
# RATE ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">💰 Rate per Sq.ft Analysis</div>',
    unsafe_allow_html=True
)


locality_rate = (
    filtered_df
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

fig_rate.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_rate,
    use_container_width=True
)


# =========================================================
# STATUS + RERA
# =========================================================

st.markdown(
    '<div class="section-title">🏗️ Property Status & RERA</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# Status
with col1:

    status_count = (
        filtered_df["Status"]
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
        use_container_width=True
    )


# RERA
with col2:

    rera_count = (
        filtered_df["RERA_Approval"]
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

    fig_rera.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig_rera,
        use_container_width=True
    )


# =========================================================
# BUILDER ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">🏢 Builder Analysis</div>',
    unsafe_allow_html=True
)


builder_count = (
    filtered_df["Builder_Name"]
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
    title="Top 10 Builders by Property Listings"
)

fig_builder.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_builder,
    use_container_width=True
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

fig_rera_price.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(
    fig_rera_price,
    use_container_width=True
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
    text_auto=True,
    title="Area vs Price Correlation",
    color_continuous_scale="Blues"
)

fig_corr.update_layout(
    template="plotly_dark",
    height=400
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
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


st.dataframe(
    filtered_df.head(100),
    use_container_width=True,
    height=500
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#9ca3af;">
        🏠 <b>NCR Real Estate Market Analysis</b><br>
        Built with Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)