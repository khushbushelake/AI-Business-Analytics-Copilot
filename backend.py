
import os
import sqlite3
import time

import pandas as pd
import streamlit as st
from google import genai


# ============================================
# Gemini Configuration
# ============================================

gemini_key = None

# Streamlit Cloud
try:
    gemini_key = st.secrets.get("GEMINI_API_KEY")
except Exception:
    pass

# Environment variable
if not gemini_key:
    gemini_key = os.environ.get("GEMINI_API_KEY")

# Google Colab fallback
if not gemini_key:
    try:
        from google.colab import userdata
        gemini_key = userdata.get("GEMINI_API_KEY")
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
    "superstore_clean.csv"
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

    context = f"""
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
"""

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

    prompt = f"""
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
"""

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
        data = df.copy()
    else:
        data = data.copy()

    # Always use the currently filtered dataset
    data = data.reset_index(drop=True)
    question_lower = question.lower()

    # ============================================
    # DETERMINISTIC BUSINESS ANSWERS
    # ============================================

    # Highest profit margin region
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

    # Most profitable category
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

    # Highest profit margin year
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

    # Business recommendations
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
            f"- Profit margin: **{lowest_category['Profit Margin %']:.2f}%**\n\n"
            f"**2. Investigate {lowest_region['Region']} performance**\n"
            f"- Profit margin: **{lowest_region['Profit Margin %']:.2f}%**\n\n"
            f"**3. Review {slowest_shipping['Ship Mode']} shipping performance**\n"
            f"- Average shipping time: **{slowest_shipping['Average_Shipping_Days']:.2f} days**"
        )

    # ============================================
    # ADDITIONAL DIRECT DATASET ANSWERS
    # ============================================

    # Highest sales region
    if "highest sales" in question_lower and "region" in question_lower:
        region_data = get_region_performance(data)
        row = region_data.loc[region_data["Sales"].idxmax()]

        return (
            f"### 📊 Highest Sales Region\n\n"
            f"**{row['Region']}** has the highest sales.\n\n"
            f"- Sales: **${row['Sales']:,.2f}**\n"
            f"- Profit: **${row['Profit']:,.2f}**\n"
            f"- Profit Margin: **{row['Profit Margin %']:.2f}%**"
        )

    # Highest sales category
    if "highest sales" in question_lower and "category" in question_lower:
        category_data = get_category_performance(data)
        row = category_data.loc[category_data["Sales"].idxmax()]

        return (
            f"### 📊 Highest Sales Category\n\n"
            f"**{row['Product Category']}** has the highest sales.\n\n"
            f"- Sales: **${row['Sales']:,.2f}**\n"
            f"- Profit: **${row['Profit']:,.2f}**\n"
            f"- Profit Margin: **{row['Profit Margin %']:.2f}%**"
        )

    # Highest profit region
    if "highest profit" in question_lower and "region" in question_lower:
        region_data = get_region_performance(data)
        row = region_data.loc[region_data["Profit"].idxmax()]

        return (
            f"### 💰 Highest Profit Region\n\n"
            f"**{row['Region']}** generated the highest profit.\n\n"
            f"- Profit: **${row['Profit']:,.2f}**\n"
            f"- Sales: **${row['Sales']:,.2f}**\n"
            f"- Profit Margin: **{row['Profit Margin %']:.2f}%**"
        )

    # Overall KPI questions
    if "total sales" in question_lower:
        kpis = get_business_kpis(data)

        return (
            f"### 💵 Total Sales\n\n"
            f"Total sales are **${kpis['total_sales']:,.2f}**."
        )

    if "total profit" in question_lower:
        kpis = get_business_kpis(data)

        return (
            f"### 💰 Total Profit\n\n"
            f"Total profit is **${kpis['total_profit']:,.2f}**."
        )

    if "average order value" in question_lower:
        total_sales = data["Sales"].sum()
        total_orders = data["Order ID"].nunique()
        aov = total_sales / total_orders if total_orders else 0

        return (
            f"### 🧾 Average Order Value\n\n"
            f"The average order value is **${aov:,.2f}**."
        )

    # Shipping questions
    if "shipping" in question_lower and (
        "fastest" in question_lower or
        "slowest" in question_lower
    ):
        shipping_data = (
            data.groupby("Ship Mode")
            .agg(
                Average_Shipping_Days=("Shipping Days", "mean"),
                Orders=("Order ID", "nunique")
            )
            .reset_index()
        )

        if "fastest" in question_lower:
            row = shipping_data.loc[
                shipping_data["Average_Shipping_Days"].idxmin()
            ]
            label = "Fastest"

        else:
            row = shipping_data.loc[
                shipping_data["Average_Shipping_Days"].idxmax()
            ]
            label = "Slowest"

        return (
            f"### 🚚 {label} Shipping Mode\n\n"
            f"**{row['Ship Mode']}** has an average shipping time of "
            f"**{row['Average_Shipping_Days']:.2f} days**.\n\n"
            f"- Orders: **{row['Orders']:,}**"
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

    prompt = f"""
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
"""

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

    prompt = f"""
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
"""

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
