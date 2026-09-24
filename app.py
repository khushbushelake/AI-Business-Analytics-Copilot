
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

    st.markdown("### 📅 Filters")

    years = sorted(
        backend.df["Year"].unique()
    )

    selected_year = st.selectbox(
        "Select Year",
        ["All Years"] + years,
        key="year_filter"
    )

    st.divider()

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

if selected_year == "All Years":

    filtered_df = backend.df.copy()

else:

    filtered_df = backend.df[
        backend.df["Year"] == selected_year
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


# Additional KPI calculations
total_customers = filtered_df["Customer Name"].nunique()

total_quantity = filtered_df["Order Quantity"].sum()

average_order_value = (
    total_sales / total_orders
    if total_orders != 0
    else 0
)


# ============================================
# ADDITIONAL BUSINESS KPIs
# ============================================

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
        f"${average_order_value:,.0f}"
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
# PROFITABILITY ANALYSIS
# ============================================

st.markdown(
    '<div class="section-title">'
    '💰 Profitability Analysis'
    '</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# --------------------------------------------
# Regional Profit
# --------------------------------------------

with col1:

    st.markdown("### Regional Profit")

    st.bar_chart(
        region_data.set_index("Region")["Profit"]
    )


# --------------------------------------------
# Category Profit
# --------------------------------------------

with col2:

    st.markdown("### Category Profit")

    st.bar_chart(
        category_data.set_index(
            "Product Category"
        )["Profit"]
    )


st.divider()


# ============================================
# AUTOMATIC BUSINESS INSIGHTS
# ============================================

st.markdown(
    '<div class="section-title">'
    '💡 Automatic Business Insights'
    '</div>',
    unsafe_allow_html=True
)

# Calculate profitability metrics
region_insights = (
    filtered_df
    .groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

region_insights["Profit Margin %"] = (
    region_insights["Profit"]
    / region_insights["Sales"]
) * 100

category_insights = (
    filtered_df
    .groupby("Product Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

category_insights["Profit Margin %"] = (
    category_insights["Profit"]
    / category_insights["Sales"]
) * 100


# Find key insights
top_profit_region = region_insights.loc[
    region_insights["Profit"].idxmax()
]

top_profit_category = category_insights.loc[
    category_insights["Profit"].idxmax()
]

top_margin_region = region_insights.loc[
    region_insights["Profit Margin %"].idxmax()
]

lowest_margin_category = category_insights.loc[
    category_insights["Profit Margin %"].idxmin()
]


# Display insights
insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.info(
        f"🏆 **Highest Profit Region:** "
        f"{top_profit_region['Region']} — "
        f"${top_profit_region['Profit']:,.0f}"
    )

    st.info(
        f"📊 **Highest Profit Category:** "
        f"{top_profit_category['Product Category']} — "
        f"${top_profit_category['Profit']:,.0f}"
    )

    st.info(
        f"📈 **Highest Regional Profit Margin:** "
        f"{top_margin_region['Region']} — "
        f"{top_margin_region['Profit Margin %']:.2f}%"
    )


with insight_col2:

    st.warning(
        f"⚠️ **Lowest Category Profit Margin:** "
        f"{lowest_margin_category['Product Category']} — "
        f"{lowest_margin_category['Profit Margin %']:.2f}%"
    )

    if (
        lowest_margin_category["Sales"]
        > top_profit_category["Sales"] * 0.75
        and lowest_margin_category["Profit Margin %"]
        < top_profit_category["Profit Margin %"]
    ):

        st.warning(
            f"💡 **Sales vs Profitability:** "
            f"{lowest_margin_category['Product Category']} "
            f"generates ${lowest_margin_category['Sales']:,.0f} "
            f"in sales but has a relatively low "
            f"profit margin of "
            f"{lowest_margin_category['Profit Margin %']:.2f}%."
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
# SHIPPING PERFORMANCE
# ============================================

st.markdown(
    '<div class="section-title">'
    '🚚 Shipping Performance'
    '</div>',
    unsafe_allow_html=True
)

shipping_data = (
    filtered_df
    .groupby("Ship Mode")
    .agg(
        Average_Shipping_Days=("Shipping Days", "mean"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

shipping_data["Average_Shipping_Days"] = (
    shipping_data["Average_Shipping_Days"].round(2)
)

col1, col2 = st.columns(2)


# --------------------------------------------
# Average Shipping Days
# --------------------------------------------

with col1:

    st.markdown("### Average Shipping Days")

    st.bar_chart(
        shipping_data.set_index("Ship Mode")[
            "Average_Shipping_Days"
        ]
    )


# --------------------------------------------
# Orders by Ship Mode
# --------------------------------------------

with col2:

    st.markdown("### Orders by Ship Mode")

    st.bar_chart(
        shipping_data.set_index("Ship Mode")[
            "Orders"
        ]
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

# --------------------------------------------
# Suggested Questions
# --------------------------------------------

st.markdown("**💬 Try asking:**")

suggestion_cols = st.columns(4)

suggested_questions = [
    "Which region has the highest profit margin?",
    "Which category generated the most profit?",
    "Which year had the highest profit margin?",
    "Give me 3 business recommendations."
]

for col, suggestion in zip(
    suggestion_cols,
    suggested_questions
):

    with col:

        if st.button(
            suggestion,
            use_container_width=True
        ):
            st.session_state["selected_question"] = suggestion


selected_question = st.session_state.get(
    "selected_question",
    ""
)

question = st.text_input(
    "Ask a business question",
    value=selected_question,
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
            question,
            filtered_df
        )

        st.markdown(
            answer
        )
