
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
