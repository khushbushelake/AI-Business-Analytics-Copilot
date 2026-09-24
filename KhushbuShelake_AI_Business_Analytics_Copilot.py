# ============================================================
# AI-Powered Business Analytics Copilot
# Author: Khushbu Shelake
# ============================================================

import types

# ============================================================
# BACKEND
# ============================================================

backend = types.ModuleType("backend")

_backend_code = r"""
import os
import sqlite3
import time

import pandas as pd
from google import genai


# ============================================
# Gemini Configuration
# ============================================

gemini_key = os.environ.get("GEMINI_API_KEY")

if not gemini_key:
    try:
        from google.colab import userdata
        gemini_key = userdata.get("GEMINI_API_KEY")
        os.environ["GEMINI_API_KEY"] = gemini_key
    except Exception:
        gemini_key = None


if gemini_key:
    gemini_client = genai.Client(
        api_key=gemini_key
    )
else:
    gemini_client = None


# Use the model that previously worked for this project.
GEMINI_MODEL = "gemini-3-flash-preview"


# ============================================
# Load Dataset
# ============================================

df = pd.read_csv(
    "/content/superstore_clean.csv"
)


# ============================================
# SQLite Database
# ============================================

conn = sqlite3.connect(
    ":memory:",
    check_same_thread=False
)

df.to_sql(
    "sales",
    conn,
    index=False,
    if_exists="replace"
)


# ============================================
# Business KPIs
# ============================================

def get_business_kpis(data):

    total_sales = data["Sales"].sum()

    total_profit = data["Profit"].sum()

    return {
        "total_sales": round(
            total_sales, 2
        ),

        "total_profit": round(
            total_profit, 2
        ),

        "total_orders": int(
            data["Order ID"].nunique()
        ),

        "total_customers": int(
            data["Customer Name"].nunique()
        ),

        "total_quantity": int(
            data["Order Quantity"].sum()
        ),

        "profit_margin": round(
            (total_profit / total_sales) * 100,
            2
        )
    }


# ============================================
# Regional Performance
# ============================================

def get_region_performance(data):

    result = (
        data
        .groupby("Region")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
    )

    result["Profit Margin %"] = (
        result["Profit"] /
        result["Sales"] *
        100
    )

    return result.sort_values(
        "Sales",
        ascending=False
    )


# ============================================
# Category Performance
# ============================================

def get_category_performance(data):

    result = (
        data
        .groupby("Product Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
    )

    result["Profit Margin %"] = (
        result["Profit"] /
        result["Sales"] *
        100
    )

    return result.sort_values(
        "Sales",
        ascending=False
    )


# ============================================
# Yearly Performance
# ============================================

def get_yearly_performance(data):

    result = (
        data
        .groupby("Year")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique"),
            Quantity=("Order Quantity", "sum")
        )
        .reset_index()
    )

    result["Profit Margin %"] = (
        result["Profit"] /
        result["Sales"] *
        100
    )

    return result


# ============================================
# Monthly Performance
# ============================================

def get_monthly_performance(data):

    result = (
        data
        .groupby("Year-Month")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
    )

    result["Profit Margin %"] = (
        result["Profit"] /
        result["Sales"] *
        100
    )

    return result


# ============================================
# Business Context
# ============================================

def build_business_context(data):

    kpis = get_business_kpis(data)

    regions = get_region_performance(data)

    categories = get_category_performance(data)

    yearly = get_yearly_performance(data)

    monthly = get_monthly_performance(data)

    context = f\"\"\"
BUSINESS ANALYTICS DATA

OVERALL KPIs
------------
Total Sales: ${kpis['total_sales']:,.2f}
Total Profit: ${kpis['total_profit']:,.2f}
Total Orders: {kpis['total_orders']:,}
Total Customers: {kpis['total_customers']:,}
Total Quantity Sold: {kpis['total_quantity']:,}
Overall Profit Margin: {kpis['profit_margin']:.2f}%

REGIONAL PERFORMANCE
--------------------
{regions.to_string(index=False)}

CATEGORY PERFORMANCE
--------------------
{categories.to_string(index=False)}

YEARLY PERFORMANCE
------------------
{yearly.to_string(index=False)}

MONTHLY PERFORMANCE
-------------------
{monthly.to_string(index=False)}
\"\"\"

    return context


business_context = build_business_context(df)


# ============================================
# Gemini AI Function
# ============================================

def ask_business_ai(
    question,
    context
):

    if gemini_client is None:

        return (
            "⚠️ Gemini API key is not available. "
            "Please configure GEMINI_API_KEY."
        )

    prompt = f\"\"\"
You are an AI Business Analytics Copilot.

Analyze the business data provided below
and answer the user's question.

RULES:
- Use only the provided business data.
- Do not invent numbers or facts.
- Explain insights in simple business language.
- Mention specific numbers when relevant.
- If the required information is not available,
  clearly say so.

BUSINESS DATA:
{context}

USER QUESTION:
{question}

Provide a useful and concise business answer.
\"\"\"

    try:

        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:

        error_text = str(e)

        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
            or "high demand" in error_text
        ):

            return (
                "⚠️ Gemini is temporarily unavailable "
                "because the AI service is experiencing "
                "high demand. Your dashboard and "
                "business data are working correctly. "
                "Please try again later."
            )

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            return (
                "⚠️ Gemini free-tier quota has been "
                "temporarily exhausted. Your dashboard "
                "and business analytics are still working "
                "correctly. Please try again after the "
                "quota resets."
            )

        return (
            f"⚠️ Unable to generate an AI answer: "
            f"{error_text}"
        )


# ============================================
# Business Copilot
# ============================================

def business_copilot(question, data=None):

    if data is None:
        data = df

    question_lower = question.lower()

    # ============================================
    # DETERMINISTIC BUSINESS ANSWERS
    # ============================================

    if "highest profit margin" in question_lower and "region" in question_lower:
        region_data = get_region_performance(data)
        row = region_data.loc[region_data["Profit Margin %"].idxmax()]

        return (
            f"### 📍 Highest Regional Profit Margin\n\n"
            f"**{row['Region']}** has the highest profit margin at "
            f"**{row['Profit Margin %']:.2f}%**.\n\n"
            f"- Sales: **${row['Sales']:,.2f}**\n"
            f"- Profit: **${row['Profit']:,.2f}**\n"
            f"- Orders: **{row['Orders']:,}**"
        )

    if "most profit" in question_lower and "category" in question_lower:
        category_data = get_category_performance(data)
        row = category_data.loc[category_data["Profit"].idxmax()]

        return (
            f"### 🏆 Most Profitable Category\n\n"
            f"**{row['Product Category']}** generated the highest profit.\n\n"
            f"- Profit: **${row['Profit']:,.2f}**\n"
            f"- Sales: **${row['Sales']:,.2f}**\n"
            f"- Profit Margin: **{row['Profit Margin %']:.2f}%**"
        )

    if "highest profit margin" in question_lower and "year" in question_lower:
        yearly_data = get_yearly_performance(data)
        row = yearly_data.loc[yearly_data["Profit Margin %"].idxmax()]

        return (
            f"### 📅 Highest Profit Margin Year\n\n"
            f"**{int(row['Year'])}** had the highest profit margin at "
            f"**{row['Profit Margin %']:.2f}%**.\n\n"
            f"- Sales: **${row['Sales']:,.2f}**\n"
            f"- Profit: **${row['Profit']:,.2f}**"
        )

    if "recommendation" in question_lower or "recommendations" in question_lower:
        region_data = get_region_performance(data)
        category_data = get_category_performance(data)

        lowest_region = region_data.loc[
            region_data["Profit Margin %"].idxmin()
        ]

        lowest_category = category_data.loc[
            category_data["Profit Margin %"].idxmin()
        ]

        shipping_data = (
            data.groupby("Ship Mode")
            .agg(
                Average_Shipping_Days=("Shipping Days", "mean"),
                Orders=("Order ID", "nunique")
            )
            .reset_index()
        )

        slowest_shipping = shipping_data.loc[
            shipping_data["Average_Shipping_Days"].idxmax()
        ]

        return (
            "### 💡 3 Business Recommendations\n\n"
            f"**1. Improve {lowest_category['Product Category']} profitability**\n"
            f"- It has the lowest category profit margin at "
            f"**{lowest_category['Profit Margin %']:.2f}%**. "
            f"Review pricing, discounts, and product-level costs.\n\n"
            f"**2. Investigate {lowest_region['Region']} performance**\n"
            f"- Its regional profit margin is "
            f"**{lowest_region['Profit Margin %']:.2f}%**. "
            f"Analyze products, customers, and discount patterns in this region.\n\n"
            f"**3. Review {slowest_shipping['Ship Mode']} shipping performance**\n"
            f"- It has the highest average shipping time at "
            f"**{slowest_shipping['Average_Shipping_Days']:.2f} days**. "
            f"Review whether delivery time can be reduced without increasing costs."
        )

    # ============================================
    # SQL / AI FALLBACK
    # ============================================

    context = build_business_context(data)

    sql_answer = sql_business_answer(
        question,
        data
    )

    if sql_answer and not sql_answer.startswith("⚠️"):
        return sql_answer

    return ask_business_ai(
        question,
        context
    )


# ============================================
# SQL Generation
# ============================================

def generate_sql(question):

    if gemini_client is None:

        return None

    prompt = f\"\"\"
You are an expert SQL analyst.

Convert the user's business question
into a SQLite SQL query.

DATABASE TABLE:
sales

Use only the sales table.

Return ONLY the SQL query.

The query must be SELECT only.

USER QUESTION:
{question}
\"\"\"

    try:

        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text.strip()

    except Exception:

        return None


# ============================================
# SQL Safety
# ============================================

def is_safe_sql(sql_query):

    if not sql_query:
        return False

    sql = sql_query.strip().lower()

    if not sql.startswith("select"):
        return False

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "detach",
        "pragma"
    ]

    for keyword in blocked_keywords:

        if keyword in sql:
            return False

    return True


# ============================================
# SQL Business Answer
# ============================================

def sql_business_answer(question, data=None):

    sql_query = generate_sql(question)

    if not is_safe_sql(sql_query):

        return (
            "⚠️ I couldn't generate a safe SQL "
            "query for this question."
        )

    try:

        # Use filtered data when provided
        if data is not None:

            temp_conn = sqlite3.connect(":memory:")

            data.to_sql(
                "sales",
                temp_conn,
                index=False,
                if_exists="replace"
            )

            result = pd.read_sql_query(
                sql_query,
                temp_conn
            )

            temp_conn.close()

        else:

            result = pd.read_sql_query(
                sql_query,
                conn
            )

    except Exception as e:

        return (
            f"⚠️ SQL execution error: {e}"
        )

    result_text = result.to_string(
        index=False
    )

    prompt = f\"\"\"
You are an AI Business Analytics Copilot.

Answer the user's business question
using the SQL result below.

USER QUESTION:
{question}

SQL RESULT:
{result_text}

RULES:
- Give a clear and concise business answer.
- Use the exact values from the SQL result.
- Do not invent additional numbers.
\"\"\"

    try:

        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text

    except Exception:

        return (
            "The SQL analysis was completed, "
            "but Gemini is temporarily unavailable "
            "to explain the result."
        )


"""

exec(_backend_code, backend.__dict__)

del _backend_code

# ============================================================
# STREAMLIT APPLICATION
# ============================================================


import streamlit as st



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


# ============================================================
# END OF PROJECT
# ============================================================
