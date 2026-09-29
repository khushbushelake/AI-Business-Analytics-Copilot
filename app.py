
import streamlit as st
import backend


# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="AI Business Analytics Copilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

.stApp {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #667085;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 650;
    margin-top: 10px;
    margin-bottom: 15px;
}

div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e4e7ec;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 2px 8px rgba(16, 24, 40, 0.05);
}

div[data-testid="stMetricLabel"] {
    font-size: 14px;
    color: #667085;
}

div[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: 700;
}

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e4e7ec;
}

</style>
""", unsafe_allow_html=True)


# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.markdown("## 📊 Analytics Copilot")

    st.write(
        "AI-powered business analytics "
        "for the Superstore dataset."
    )

    st.divider()

    # ============================================
    # INTERACTIVE FILTERS
    # ============================================

    st.markdown("### 🔎 Filters")

    years = sorted(
        backend.df["Year"].unique()
    )

    regions = sorted(
        backend.df["Region"].dropna().unique()
    )

    categories = sorted(
        backend.df["Product Category"].dropna().unique()
    )

    segments = sorted(
        backend.df["Customer Segment"].dropna().unique()
    )

    ship_modes = sorted(
        backend.df["Ship Mode"].dropna().unique()
    )

    selected_year = st.selectbox(
        "📅 Select Year",
        ["All Years"] + years,
        key="year_filter"
    )

    selected_region = st.multiselect(
        "🌎 Region",
        regions,
        default=regions,
        key="region_filter"
    )

    selected_category = st.multiselect(
        "📦 Category",
        categories,
        default=categories,
        key="category_filter"
    )

    selected_segment = st.multiselect(
        "👥 Customer Segment",
        segments,
        default=segments,
        key="segment_filter"
    )

    selected_ship_mode = st.multiselect(
        "🚚 Ship Mode",
        ship_modes,
        default=ship_modes,
        key="ship_mode_filter"
    )

    st.divider()

    # ============================================
    # TECHNOLOGY
    # ============================================

    st.markdown("### 🛠️ Technology")

    st.write("🐍 Python")
    st.write("🐼 Pandas")
    st.write("🗄️ SQLite")
    st.write("🤖 Google Gemini")
    st.write("📊 Streamlit")

    st.divider()

    st.caption("AI Business Analytics Copilot")
    st.caption("Portfolio Project")


# ============================================
# FILTER DATA
# ============================================

filtered_df = backend.df.copy()

if selected_year != "All Years":

    filtered_df = filtered_df[
        filtered_df["Year"] == selected_year
    ]

filtered_df = filtered_df[
    filtered_df["Region"].isin(selected_region)
    &
    filtered_df["Product Category"].isin(selected_category)
    &
    filtered_df["Customer Segment"].isin(selected_segment)
    &
    filtered_df["Ship Mode"].isin(selected_ship_mode)
].copy()
# ============================================
# HEADER
# ============================================

st.markdown(
    '<div class="main-title">'
    '📊 AI Business Analytics Copilot'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Turn business data into actionable insights using AI.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================
# KPI CALCULATIONS
# ============================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()

if total_sales != 0:

    profit_margin = (
        total_profit / total_sales
    ) * 100

else:

    profit_margin = 0


# ============================================
# BUSINESS SNAPSHOT
# ============================================

st.markdown(
    '<div class="section-title">'
    '📌 Business Snapshot'
    '</div>',
    unsafe_allow_html=True
)

# Additional KPI calculations
total_customers = filtered_df["Customer Name"].nunique()

total_quantity = filtered_df["Order Quantity"].sum()

average_order_value = (
    total_sales / total_orders
    if total_orders != 0 else 0
)

# KPI Row 1
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"${total_sales:,.0f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${total_profit:,.0f}"
    )

with col3:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col4:
    st.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )

# KPI Row 2
col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col6:
    st.metric(
        "Quantity Sold",
        f"{total_quantity:,}"
    )

with col7:
    st.metric(
        "Average Order Value",
        f"${average_order_value:,.2f}"
    )

st.divider()


# ============================================
# BUSINESS OVERVIEW
# ============================================

st.markdown(
    '<div class="section-title">'
    '📈 Business Overview'
    '</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# --------------------------------------------
# Regional Sales
# --------------------------------------------

with col1:

    region_data = (
        filtered_df
        .groupby("Region")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    st.markdown("### Regional Sales")

    st.bar_chart(
        region_data.set_index("Region")["Sales"]
    )


# --------------------------------------------
# Category Sales
# --------------------------------------------

with col2:

    category_data = (
        filtered_df
        .groupby("Product Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    st.markdown("### Category Sales")

    st.bar_chart(
        category_data.set_index(
            "Product Category"
        )["Sales"]
    )


st.divider()


# ============================================
# MONTHLY PERFORMANCE TREND
# ============================================

st.markdown(
    '<div class="section-title">'
    '📅 Monthly Performance Trend'
    '</div>',
    unsafe_allow_html=True
)

monthly_data = (
    filtered_df
    .groupby("Year-Month")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

monthly_data = monthly_data.sort_values(
    "Year-Month"
)

st.line_chart(
    monthly_data.set_index("Year-Month")[
        ["Sales", "Profit"]
    ]
)


st.divider()


# ============================================
# EXECUTIVE BUSINESS INSIGHTS
# ============================================

import pandas as pd

# ============================================
# KPI TREND INDICATORS
# ============================================

st.markdown(
    '<div class="section-title">'
    '🎯 KPI Performance Indicators'
    '</div>',
    unsafe_allow_html=True
)

# Current filtered KPIs
current_sales = filtered_df["Sales"].sum()
current_profit = filtered_df["Profit"].sum()
current_orders = filtered_df["Order ID"].nunique()

if current_sales != 0:
    current_margin = (
        current_profit / current_sales
    ) * 100
else:
    current_margin = 0


# Calculate previous-period comparison
if selected_year == "All Years":

    yearly_kpi = (
        backend.df
        .groupby("Year")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
        .sort_values("Year")
    )

    if len(yearly_kpi) >= 2:

        latest = yearly_kpi.iloc[-1]
        previous = yearly_kpi.iloc[-2]

        sales_change = (
            (latest["Sales"] - previous["Sales"])
            / previous["Sales"] * 100
        )

        profit_change = (
            (latest["Profit"] - previous["Profit"])
            / previous["Profit"] * 100
        )

        orders_change = (
            (latest["Orders"] - previous["Orders"])
            / previous["Orders"] * 100
        )

        previous_margin = (
            previous["Profit"]
            / previous["Sales"] * 100
        )

        margin_change = (
            current_margin - previous_margin
        )

    else:

        sales_change = 0
        profit_change = 0
        orders_change = 0
        margin_change = 0

else:

    # Compare selected year with previous year
    selected_year_int = int(selected_year)

    current_year_data = backend.df[
        backend.df["Year"] == selected_year_int
    ]

    previous_year_data = backend.df[
        backend.df["Year"] == selected_year_int - 1
    ]

    if len(previous_year_data) > 0:

        previous_sales = previous_year_data["Sales"].sum()
        previous_profit = previous_year_data["Profit"].sum()
        previous_orders = previous_year_data["Order ID"].nunique()

        previous_margin = (
            previous_profit / previous_sales * 100
            if previous_sales != 0 else 0
        )

        sales_change = (
            (current_sales - previous_sales)
            / previous_sales * 100
            if previous_sales != 0 else 0
        )

        profit_change = (
            (current_profit - previous_profit)
            / previous_profit * 100
            if previous_profit != 0 else 0
        )

        orders_change = (
            (current_orders - previous_orders)
            / previous_orders * 100
            if previous_orders != 0 else 0
        )

        margin_change = (
            current_margin - previous_margin
        )

    else:

        sales_change = 0
        profit_change = 0
        orders_change = 0
        margin_change = 0


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Sales",
        f"${current_sales:,.0f}",
        f"{sales_change:+.2f}%"
    )

with col2:

    st.metric(
        "Profit",
        f"${current_profit:,.0f}",
        f"{profit_change:+.2f}%"
    )

with col3:

    st.metric(
        "Orders",
        f"{current_orders:,}",
        f"{orders_change:+.2f}%"
    )

with col4:

    st.metric(
        "Profit Margin",
        f"{current_margin:.2f}%",
        f"{margin_change:+.2f} pp"
    )


# ============================================
# PROFITABILITY MATRIX
# ============================================

st.markdown(
    '<div class="section-title">'
    '📊 Profitability Matrix'
    '</div>',
    unsafe_allow_html=True
)

matrix_data = (
    filtered_df
    .groupby("Product Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

matrix_data["Profit Margin %"] = (
    matrix_data["Profit"]
    / matrix_data["Sales"]
    * 100
)

if len(matrix_data) > 0:

    sales_median = matrix_data["Sales"].median()
    profit_median = matrix_data["Profit"].median()

    def classify_category(row):

        if (
            row["Sales"] >= sales_median
            and row["Profit"] >= profit_median
        ):
            return "High Sales / High Profit"

        elif (
            row["Sales"] >= sales_median
            and row["Profit"] < profit_median
        ):
            return "High Sales / Low Profit"

        elif (
            row["Sales"] < sales_median
            and row["Profit"] >= profit_median
        ):
            return "Low Sales / High Profit"

        else:
            return "Low Sales / Low Profit"

    matrix_data["Performance Segment"] = (
        matrix_data.apply(
            classify_category,
            axis=1
        )
    )

    st.dataframe(
        matrix_data[
            [
                "Product Category",
                "Sales",
                "Profit",
                "Profit Margin %",
                "Performance Segment"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Categories are classified using median Sales and "
        "Profit as the comparison thresholds."
    )


# ============================================
# EXECUTIVE SUMMARY
# ============================================

st.markdown(
    '<div class="section-title">'
    '💡 Executive Business Summary'
    '</div>',
    unsafe_allow_html=True
)

# Regional insight
region_summary = (
    filtered_df
    .groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

region_summary["Profit Margin %"] = (
    region_summary["Profit"]
    / region_summary["Sales"]
    * 100
)

if len(region_summary) > 0:

    top_sales_region = region_summary.loc[
        region_summary["Sales"].idxmax()
    ]

    top_profit_region = region_summary.loc[
        region_summary["Profit"].idxmax()
    ]

    top_margin_region = region_summary.loc[
        region_summary["Profit Margin %"].idxmax()
    ]

else:

    top_sales_region = None
    top_profit_region = None
    top_margin_region = None


# Category insight
category_summary = (
    filtered_df
    .groupby("Product Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

category_summary["Profit Margin %"] = (
    category_summary["Profit"]
    / category_summary["Sales"]
    * 100
)

if len(category_summary) > 0:

    top_profit_category = category_summary.loc[
        category_summary["Profit"].idxmax()
    ]

    lowest_margin_category = category_summary.loc[
        category_summary["Profit Margin %"].idxmin()
    ]

else:

    top_profit_category = None
    lowest_margin_category = None


if (
    top_sales_region is not None
    and top_profit_region is not None
    and top_profit_category is not None
):

    period_text = (
        "the complete dataset"
        if selected_year == "All Years"
        else f"{selected_year}"
    )

    st.info(
        f"""
        **Business Summary — {period_text}**

        • **Sales Leader:** {top_sales_region['Region']}
        generated ${top_sales_region['Sales']:,.0f} in sales.

        • **Profit Leader by Region:** {top_profit_region['Region']}
        generated ${top_profit_region['Profit']:,.0f} in profit.

        • **Highest Profit Margin Region:**
        {top_margin_region['Region']} with a
        {top_margin_region['Profit Margin %']:.2f}% margin.

        • **Most Profitable Category:**
        {top_profit_category['Product Category']} with
        ${top_profit_category['Profit']:,.0f} profit.

        • **Lowest Category Margin:**
        {lowest_margin_category['Product Category']} at
        {lowest_margin_category['Profit Margin %']:.2f}%.
        """
    )


st.divider()# ============================================
# QUARTERLY & CUSTOMER PROFITABILITY ANALYSIS
# ============================================

import pandas as pd

# ============================================
# QUARTERLY PERFORMANCE ANALYSIS
# ============================================

st.markdown(
    '<div class="section-title">'
    '📅 Quarterly Performance Analysis'
    '</div>',
    unsafe_allow_html=True
)

quarter_data = (
    filtered_df
    .groupby("Quarter")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Order Quantity", "sum")
    )
    .reset_index()
)

quarter_data["Profit Margin %"] = (
    quarter_data["Profit"]
    / quarter_data["Sales"]
    * 100
)

# Keep quarters in correct order
quarter_order = ["Q1", "Q2", "Q3", "Q4"]

quarter_data["Quarter"] = pd.Categorical(
    quarter_data["Quarter"],
    categories=quarter_order,
    ordered=True
)

quarter_data = quarter_data.sort_values("Quarter")

col1, col2 = st.columns(2)

with col1:

    st.markdown("**Sales by Quarter**")

    st.bar_chart(
        quarter_data.set_index("Quarter")["Sales"]
    )

with col2:

    st.markdown("**Profit by Quarter**")

    st.bar_chart(
        quarter_data.set_index("Quarter")["Profit"]
    )

st.dataframe(
    quarter_data[
        [
            "Quarter",
            "Sales",
            "Profit",
            "Orders",
            "Quantity",
            "Profit Margin %"
        ]
    ].round(2),
    use_container_width=True,
    hide_index=True
)


# ============================================
# TOP & BOTTOM PRODUCT RANKING
# ============================================

st.markdown(
    '<div class="section-title">'
    '🏆 Product Profitability Ranking'
    '</div>',
    unsafe_allow_html=True
)

product_ranking = (
    filtered_df
    .groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

product_ranking["Profit Margin %"] = (
    product_ranking["Profit"]
    / product_ranking["Sales"]
    * 100
)

top_products = (
    product_ranking
    .sort_values("Profit", ascending=False)
    .head(10)
)

bottom_products = (
    product_ranking
    .sort_values("Profit", ascending=True)
    .head(10)
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("**Top 10 Products by Profit**")

    st.dataframe(
        top_products[
            [
                "Product Name",
                "Sales",
                "Profit",
                "Profit Margin %"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

with col2:

    st.markdown("**Bottom 10 Products by Profit**")

    st.dataframe(
        bottom_products[
            [
                "Product Name",
                "Sales",
                "Profit",
                "Profit Margin %"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )


# ============================================
# CUSTOMER PROFITABILITY ANALYSIS
# ============================================

st.markdown(
    '<div class="section-title">'
    '💼 Customer Profitability Analysis'
    '</div>',
    unsafe_allow_html=True
)

customer_profit = (
    filtered_df
    .groupby("Customer Name")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Order Quantity", "sum")
    )
    .reset_index()
)

customer_profit["Profit Margin %"] = (
    customer_profit["Profit"]
    / customer_profit["Sales"]
    * 100
)

top_customers = (
    customer_profit
    .sort_values("Profit", ascending=False)
    .head(10)
)

loss_customers = (
    customer_profit[
        customer_profit["Profit"] < 0
    ]
    .sort_values("Profit", ascending=True)
    .head(10)
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("**Top 10 Customers by Profit**")

    st.dataframe(
        top_customers[
            [
                "Customer Name",
                "Sales",
                "Profit",
                "Orders",
                "Profit Margin %"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

with col2:

    st.markdown("**Loss-Making Customers**")

    if len(loss_customers) > 0:

        st.dataframe(
            loss_customers[
                [
                    "Customer Name",
                    "Sales",
                    "Profit",
                    "Orders",
                    "Profit Margin %"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "✅ No loss-making customers found."
        )


# ============================================
# AUTOMATIC QUARTER & CUSTOMER INSIGHTS
# ============================================

if len(quarter_data) > 0:

    best_quarter = quarter_data.loc[
        quarter_data["Profit"].idxmax()
    ]

    best_margin_quarter = quarter_data.loc[
        quarter_data["Profit Margin %"].idxmax()
    ]

    st.info(
        f"💡 **Quarterly Insight:** "
        f"{best_quarter['Quarter']} generated the highest "
        f"profit at ${best_quarter['Profit']:,.0f}, while "
        f"{best_margin_quarter['Quarter']} had the highest "
        f"profit margin at "
        f"{best_margin_quarter['Profit Margin %']:.2f}%."
    )


if len(customer_profit) > 0:

    best_customer = customer_profit.loc[
        customer_profit["Profit"].idxmax()
    ]

    st.info(
        f"💡 **Customer Insight:** "
        f"{best_customer['Customer Name']} generated the "
        f"highest profit at "
        f"${best_customer['Profit']:,.0f}."
    )


st.divider()


# ============================================
# REGIONAL, SHIPPING & GROWTH ANALYSIS
# ============================================

import pandas as pd

# ============================================
# REGIONAL × CATEGORY ANALYSIS
# ============================================

st.markdown(
    '<div class="section-title">'
    '🌍 Regional × Category Analysis'
    '</div>',
    unsafe_allow_html=True
)

region_category = (
    filtered_df
    .groupby(["Region", "Product Category"])
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

region_category["Profit Margin %"] = (
    region_category["Profit"]
    / region_category["Sales"]
    * 100
)

st.dataframe(
    region_category[
        [
            "Region",
            "Product Category",
            "Sales",
            "Profit",
            "Orders",
            "Profit Margin %"
        ]
    ]
    .sort_values("Sales", ascending=False)
    .round(2),
    use_container_width=True,
    hide_index=True
)

# Top region-category combinations
top_region_category = (
    region_category
    .sort_values("Profit", ascending=False)
    .head(10)
)

st.markdown("**Top 10 Region–Category Combinations by Profit**")

st.bar_chart(
    top_region_category.set_index(
        "Region"
    )["Profit"]
)


# ============================================
# SHIPPING EFFICIENCY ANALYSIS
# ============================================

st.markdown(
    '<div class="section-title">'
    '🚚 Shipping Efficiency Analysis'
    '</div>',
    unsafe_allow_html=True
)

shipping_efficiency = (
    filtered_df
    .groupby("Ship Mode")
    .agg(
        Average_Shipping_Days=("Shipping Days", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

shipping_efficiency["Profit Margin %"] = (
    shipping_efficiency["Profit"]
    / shipping_efficiency["Sales"]
    * 100
)

shipping_efficiency = shipping_efficiency.sort_values(
    "Average_Shipping_Days"
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("**Average Shipping Days**")

    st.bar_chart(
        shipping_efficiency.set_index(
            "Ship Mode"
        )["Average_Shipping_Days"]
    )

with col2:

    st.markdown("**Profit by Shipping Mode**")

    st.bar_chart(
        shipping_efficiency.set_index(
            "Ship Mode"
        )["Profit"]
    )

st.dataframe(
    shipping_efficiency[
        [
            "Ship Mode",
            "Average_Shipping_Days",
            "Sales",
            "Profit",
            "Orders",
            "Profit Margin %"
        ]
    ].round(2),
    use_container_width=True,
    hide_index=True
)


# ============================================
# YEAR-OVER-YEAR GROWTH ANALYSIS
# ============================================

st.markdown(
    '<div class="section-title">'
    '📈 Year-over-Year Growth Analysis'
    '</div>',
    unsafe_allow_html=True
)

year_growth = (
    backend.df
    .groupby("Year")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
    .sort_values("Year")
)

# Calculate growth percentages
year_growth["Sales Growth %"] = (
    year_growth["Sales"]
    .pct_change()
    * 100
)

year_growth["Profit Growth %"] = (
    year_growth["Profit"]
    .pct_change()
    * 100
)

year_growth["Orders Growth %"] = (
    year_growth["Orders"]
    .pct_change()
    * 100
)

# Replace first year's missing growth with 0
year_growth[
    [
        "Sales Growth %",
        "Profit Growth %",
        "Orders Growth %"
    ]
] = year_growth[
    [
        "Sales Growth %",
        "Profit Growth %",
        "Orders Growth %"
    ]
].fillna(0)

st.dataframe(
    year_growth[
        [
            "Year",
            "Sales",
            "Profit",
            "Orders",
            "Sales Growth %",
            "Profit Growth %",
            "Orders Growth %"
        ]
    ].round(2),
    use_container_width=True,
    hide_index=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("**Yearly Sales Growth**")

    st.bar_chart(
        year_growth.set_index("Year")[
            "Sales Growth %"
        ]
    )

with col2:

    st.markdown("**Yearly Profit Growth**")

    st.bar_chart(
        year_growth.set_index("Year")[
            "Profit Growth %"
        ]
    )


# ============================================
# AUTOMATIC GROWTH INSIGHT
# ============================================

if len(year_growth) >= 2:

    latest_year = year_growth.iloc[-1]
    previous_year = year_growth.iloc[-2]

    if latest_year["Sales Growth %"] > 0:

        sales_message = (
            f"Sales increased by "
            f"{latest_year['Sales Growth %']:.2f}% "
            f"from {int(previous_year['Year'])} to "
            f"{int(latest_year['Year'])}."
        )

    else:

        sales_message = (
            f"Sales decreased by "
            f"{abs(latest_year['Sales Growth %']):.2f}% "
            f"from {int(previous_year['Year'])} to "
            f"{int(latest_year['Year'])}."
        )

    if latest_year["Profit Growth %"] > 0:

        profit_message = (
            f"Profit increased by "
            f"{latest_year['Profit Growth %']:.2f}%."
        )

    else:

        profit_message = (
            f"Profit decreased by "
            f"{abs(latest_year['Profit Growth %']):.2f}%."
        )

    st.info(
        f"💡 **Year-over-Year Insight:** "
        f"{sales_message} {profit_message}"
    )


st.divider()


# ============================================
# AI BUSINESS COPILOT
# ============================================

st.markdown(
    '<div class="section-title">'
    '🤖 AI Business Copilot'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Ask questions about sales, profit, regions, "
    "categories and business performance."
)

question = st.text_input(
    "Ask a business question",
    placeholder=(
        "Example: Which region has the highest "
        "profit margin?"
    ),
    key="business_question"
)


if question:

    with st.spinner(
        "🤖 Analyzing your business data..."
    ):

        answer = backend.business_copilot(
            question
        )

        st.success(answer)



# ============================================
# RISK & OPPORTUNITY DETECTION
# ============================================

st.markdown(
    '<div class="section-title">'
    '⚠️ Risk & Opportunity Detection'
    '</div>',
    unsafe_allow_html=True
)

risk_col1, risk_col2 = st.columns(2)

# Category-level risk analysis
risk_category = (
    filtered_df
    .groupby("Product Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

risk_category["Profit Margin %"] = (
    risk_category["Profit"]
    / risk_category["Sales"]
    * 100
)

with risk_col1:

    st.markdown("### ⚠️ Business Risks")

    risks = []

    # Low-margin high-sales category
    if len(risk_category) > 0:

        median_sales = risk_category["Sales"].median()

        high_sales_low_margin = risk_category[
            (risk_category["Sales"] >= median_sales) &
            (risk_category["Profit Margin %"] < 5)
        ]

        for _, row in high_sales_low_margin.iterrows():

            risks.append(
                f"**{row['Product Category']}** has high sales "
                f"but only **{row['Profit Margin %']:.2f}%** profit margin."
            )

    # Loss-making products
    loss_products = filtered_df[
        filtered_df["Profit"] < 0
    ]

    if len(loss_products) > 0:

        loss_count = loss_products["Product Name"].nunique()

        risks.append(
            f"**{loss_count:,} products** have recorded "
            f"loss-making transactions."
        )

    # Loss-making customers
    customer_profit = (
        filtered_df
        .groupby("Customer Name")["Profit"]
        .sum()
    )

    loss_customers = customer_profit[
        customer_profit < 0
    ]

    if len(loss_customers) > 0:

        risks.append(
            f"**{len(loss_customers):,} customers** have "
            f"negative overall profit."
        )

    if risks:

        for risk in risks[:5]:
            st.warning(risk)

    else:

        st.success(
            "No major profitability risks detected "
            "in the current filtered data."
        )


with risk_col2:

    st.markdown("### 🚀 Business Opportunities")

    opportunities = []

    # Highest-margin category
    if len(risk_category) > 0:

        top_margin = risk_category.loc[
            risk_category["Profit Margin %"].idxmax()
        ]

        opportunities.append(
            f"**{top_margin['Product Category']}** has the highest "
            f"category profit margin at "
            f"**{top_margin['Profit Margin %']:.2f}%**."
        )

    # Highest-profit region
    opportunity_region = (
        filtered_df
        .groupby("Region")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    if len(opportunity_region) > 0:

        opportunity_region["Margin %"] = (
            opportunity_region["Profit"]
            / opportunity_region["Sales"]
            * 100
        )

        top_region = opportunity_region.loc[
            opportunity_region["Margin %"].idxmax()
        ]

        opportunities.append(
            f"**{top_region['Region']}** has the highest regional "
            f"profit margin at **{top_region['Margin %']:.2f}%**."
        )

    # Highest-profit customer segment
    segment_profit = (
        filtered_df
        .groupby("Customer Segment")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    if len(segment_profit) > 0:

        top_segment = segment_profit.index[0]

        opportunities.append(
            f"**{top_segment}** generates the highest total "
            f"profit among customer segments."
        )

    if opportunities:

        for opportunity in opportunities[:5]:
            st.success(opportunity)

    else:

        st.info(
            "No specific opportunities detected "
            "in the current filtered data."
        )


# ============================================
# AUTOMATIC BUSINESS RECOMMENDATIONS
# ============================================

st.markdown(
    '<div class="section-title">'
    '💡 Automatic Business Recommendations'
    '</div>',
    unsafe_allow_html=True
)

recommendations = []

# Recommendation 1: Low margin category
if len(risk_category) > 0:

    low_margin_category = risk_category.loc[
        risk_category["Profit Margin %"].idxmin()
    ]

    recommendations.append(
        f"**Review {low_margin_category['Product Category']} "
        f"profitability:** its current profit margin is "
        f"**{low_margin_category['Profit Margin %']:.2f}%**. "
        f"Consider reviewing discount levels, pricing, and product mix."
    )


# Recommendation 2: Strong category
if len(risk_category) > 0:

    high_profit_category = risk_category.loc[
        risk_category["Profit"].idxmax()
    ]

    recommendations.append(
        f"**Expand the {high_profit_category['Product Category']} "
        f"category:** it currently generates the highest category "
        f"profit of **${high_profit_category['Profit']:,.0f}**."
    )


# Recommendation 3: Regional opportunity
if len(opportunity_region) > 0:

    highest_margin_region = opportunity_region.loc[
        opportunity_region["Margin %"].idxmax()
    ]

    recommendations.append(
        f"**Study the {highest_margin_region['Region']} region:** "
        f"it achieves a **{highest_margin_region['Margin %']:.2f}%** "
        f"profit margin and may provide useful practices for other regions."
    )


# Recommendation 4: Discount risk
if "Discount" in filtered_df.columns:

    discount_analysis = (
        filtered_df
        .groupby("Discount")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    discount_analysis["Margin %"] = (
        discount_analysis["Profit"]
        / discount_analysis["Sales"]
        * 100
    )

    if len(discount_analysis) > 0:

        worst_discount = discount_analysis.loc[
            discount_analysis["Margin %"].idxmin()
        ]

        recommendations.append(
            f"**Review discount level "
            f"{worst_discount['Discount']:.0%}:** it has the lowest "
            f"profit margin at **{worst_discount['Margin %']:.2f}%**."
        )


for i, recommendation in enumerate(
    recommendations[:5],
    start=1
):

    st.info(
        f"**Recommendation {i}:** {recommendation}"
    )


# ============================================
# DATA QUALITY OVERVIEW
# ============================================

st.markdown(
    '<div class="section-title">'
    '🔎 Data Quality Overview'
    '</div>',
    unsafe_allow_html=True
)

quality_col1, quality_col2, quality_col3, quality_col4 = st.columns(4)

with quality_col1:

    st.metric(
        "Rows",
        f"{len(backend.df):,}"
    )

with quality_col2:

    st.metric(
        "Columns",
        f"{len(backend.df.columns):,}"
    )

with quality_col3:

    duplicate_count = backend.df.duplicated().sum()

    st.metric(
        "Duplicate Rows",
        f"{duplicate_count:,}"
    )

with quality_col4:

    missing_count = backend.df.isna().sum().sum()

    st.metric(
        "Missing Values",
        f"{missing_count:,}"
    )


date_col1, date_col2 = st.columns(2)

with date_col1:

    min_date = pd.to_datetime(backend.df["Order Date"]).min()

    st.metric(
        "Data Start",
        min_date.strftime("%d %b %Y")
    )

with date_col2:

    max_date = pd.to_datetime(backend.df["Order Date"]).max()

    st.metric(
        "Data End",
        max_date.strftime("%d %b %Y")
    )

st.caption(
    "Data quality metrics are calculated using the complete "
    "dataset, while business risks and recommendations use "
    "the currently selected filters."
)

st.divider()


# ============================================
# DOWNLOAD REPORTS
# ============================================

st.markdown(
    '<div class="section-title">'
    '📥 Download Reports'
    '</div>',
    unsafe_allow_html=True
)

download_col1, download_col2 = st.columns(2)

# Filtered dataset
filtered_csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

with download_col1:
    st.download_button(
        label="⬇️ Download Filtered Data",
        data=filtered_csv,
        file_name="filtered_business_data.csv",
        mime="text/csv"
    )

# Business summary
summary_data = pd.DataFrame({
    "Metric": [
        "Total Sales",
        "Total Profit",
        "Total Orders",
        "Total Customers",
        "Profit Margin",
        "Average Order Value"
    ],
    "Value": [
        round(total_sales, 2),
        round(total_profit, 2),
        total_orders,
        total_customers,
        round(profit_margin, 2),
        round(average_order_value, 2)
    ]
})

summary_csv = summary_data.to_csv(
    index=False
).encode("utf-8")

with download_col2:
    st.download_button(
        label="⬇️ Download Business Summary",
        data=summary_csv,
        file_name="business_summary.csv",
        mime="text/csv"
    )
