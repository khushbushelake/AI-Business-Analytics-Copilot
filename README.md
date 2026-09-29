# 🤖 AI-Powered Business Analytics Copilot

An interactive **AI-powered business analytics dashboard** that combines **Data Analytics, SQL, Business Intelligence, and Generative AI** to transform the Tableau Sample Superstore dataset into actionable business insights.

The application enables users to explore sales, profit, customers, products, regions, shipping, discounts, and business performance through an interactive Streamlit dashboard and a natural-language **AI Business Copilot**.

---

## 🚀 Project Highlights

- 📊 Interactive Business Analytics Dashboard
- 🤖 AI Business Copilot using Google Gemini
- 💰 Sales & Profitability Analysis
- 🌎 Regional & Category Performance
- 📈 Monthly, Quarterly & Yearly Trends
- 👥 Customer & Customer Segment Analysis
- 📦 Product & Sub-Category Analysis
- 🚚 Shipping Performance & Efficiency
- 🎯 Discount & Profitability Analysis
- 🔍 Anomaly Detection
- 🔮 Business Forecasting
- ⚠️ Risk & Opportunity Detection
- 💡 Automatic Business Recommendations
- 📊 Profitability Matrix
- 📈 Year-over-Year Growth Analysis
- 🏆 Top & Bottom Product Rankings
- 🗺️ State-Level Performance Analysis
- 📋 Data Quality Overview
- 📥 Downloadable Business Reports

---

## 📌 Project Overview

The **AI Business Analytics Copilot** is designed to help users analyze business data without manually writing complex queries or navigating multiple analytical tools.

Users can:

1. Filter business data interactively.
2. Monitor important business KPIs.
3. Analyze regional and category performance.
4. Identify profitable and loss-making products.
5. Analyze customers and customer segments.
6. Understand shipping and discount impacts.
7. Detect business risks and opportunities.
8. Generate automatic business recommendations.
9. Ask business questions using natural language through the AI Copilot.
10. Download filtered datasets and business summaries.

---

## 📊 Key Business KPIs

The cleaned dataset contains:

| Metric | Value |
|---|---:|
| Total Sales | $14,915,600.82 |
| Total Profit | $1,521,767.96 |
| Total Orders | 5,496 |
| Total Customers | 795 |
| Total Quantity Sold | 214,777 |
| Overall Profit Margin | 10.20% |

---

## 🧠 AI Business Copilot

The project includes a natural-language **Business Copilot** powered by Google Gemini.

Users can ask questions such as:

```text
Which region has the highest profit margin?
```

```text
Which category is most profitable?
```

```text
Which region has the highest sales?
```

```text
What are the main business recommendations?
```

The system combines:

- Deterministic business analytics
- SQL-based analysis
- SQLite
- Natural-language processing
- Google Gemini
- Business insight generation

This allows users to interact with business data using natural-language questions.

---

## 📈 Dashboard Analytics

### Business Snapshot

Provides an overview of:

- Total Sales
- Total Profit
- Total Orders
- Total Customers
- Profit Margin
- Quantity Sold
- Average Order Value

### Regional Analysis

Analyze:

- Regional Sales
- Regional Profit
- Regional Profit Margin
- Regional Orders
- Regional × Category performance

### Category Analysis

Analyze:

- Technology
- Furniture
- Office Supplies
- Sales
- Profit
- Orders
- Profit Margin

### Time-Based Analysis

Includes:

- Monthly Performance
- Quarterly Performance
- Yearly Performance
- Year-over-Year Growth
- KPI Trend Indicators

### Product Analytics

Includes:

- Product Performance
- Top Products
- Bottom Products
- Product Profitability
- Loss-Making Products
- Sub-Category Performance
- Product Portfolio Summary

### Customer Analytics

Includes:

- Customer Performance
- Customer Profitability
- Customer Segments
- High-value customers
- Loss-making customers

### Shipping Analytics

Includes:

- Shipping Performance
- Shipping Efficiency
- Shipping Days
- Ship Mode analysis

### Discount & Profitability

Analyzes the relationship between:

- Discount
- Sales
- Profit
- Profit Margin

---

## ⚠️ Risk & Opportunity Detection

The dashboard automatically identifies important business situations such as:

- Categories with high sales but low profitability
- Loss-making transactions
- Loss-making customers
- High-margin categories
- High-margin regions
- High-profit customer segments
- Discount levels associated with poor profitability

---

## 💡 Automatic Business Recommendations

The system generates recommendations based on the analytical results.

Examples include:

- Reviewing low-margin product categories
- Identifying opportunities in high-margin categories
- Investigating regional profitability
- Reviewing high-discount transactions
- Monitoring loss-making products and customers

---

## 🔍 Anomaly Detection

The dashboard includes anomaly analysis to help identify unusual business performance and potentially problematic transactions or patterns.

---

## 🔮 Forecasting

Historical business performance is analyzed to provide forecasting insights and help understand potential future trends.

---

## 📋 Data Quality Overview

The final analytical dataset contains:

- **8,399 rows**
- **30 columns**
- **0 duplicate rows**
- **0 missing values after preprocessing**
- Order dates ranging from **2012 to 2015**

The data was cleaned and transformed before being used in the dashboard.

---

## 🗂️ Dataset

### Source

**Tableau Sample Superstore Dataset**

### Final Dataset

```text
Rows: 8,399
Columns: 30
Date Range: 2012–2015
```

The project includes the cleaned dataset:

```text
superstore_clean.csv
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Pandas | Data manipulation & analysis |
| NumPy | Numerical operations |
| SQLite | SQL-based business analysis |
| Streamlit | Interactive dashboard |
| Google Gemini API | Generative AI |
| Tableau Hyper API | Dataset extraction |
| Google Colab | Development environment |

---

## 📁 Project Structure

```text
AI-Business-Analytics-Copilot/
│
├── app.py
├── backend.py
├── superstore_clean.csv
├── requirements.txt
├── README.md
└── KhushbuShelake_AI_Business_Analytics_Copilot_ProjectReport.docx
```

### `app.py`

Contains the Streamlit dashboard and user interface.

### `backend.py`

Contains:

- Data loading
- KPI calculations
- Business analytics
- SQL analysis
- AI Business Copilot logic
- Business insights

### `superstore_clean.csv`

Cleaned and feature-engineered Superstore dataset.

### `requirements.txt`

Contains the Python dependencies required to run the application.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/khushbushelake/AI-Business-Analytics-Copilot.git
```

### 2. Navigate to the Project

```bash
cd AI-Business-Analytics-Copilot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔐 Google Gemini API Configuration

The AI Business Copilot uses the **Google Gemini API**.

For local execution, configure your Gemini API key using an environment variable or Streamlit Secrets.

### Streamlit Secrets

Create:

```text
.streamlit/secrets.toml
```

and add:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

### Important

**Never upload your API key to GitHub.**

Do not hard-code API keys inside:

```text
app.py
backend.py
```

---

## ☁️ Streamlit Deployment

The application can be deployed using **Streamlit Community Cloud**.

Deployment configuration:

```text
Repository:
khushbushelake/AI-Business-Analytics-Copilot

Branch:
main

Main file:
app.py
```

Add the Gemini API key through the deployment platform's Secrets configuration.

---

## 📥 Downloadable Reports

The dashboard provides downloadable reports including:

### Filtered Business Data

```text
filtered_business_data.csv
```

Contains the currently filtered dataset.

### Business Summary

```text
business_summary.csv
```

Contains key business KPIs such as:

- Total Sales
- Total Profit
- Total Orders
- Total Customers
- Profit Margin
- Average Order Value

---

## 🎯 Business Use Cases

This project demonstrates how analytics and Generative AI can support:

- Sales analysis
- Profitability analysis
- Business performance monitoring
- Customer analysis
- Product analysis
- Regional analysis
- Operational analysis
- Business decision support
- Automated insight generation

---

## 🎓 Skills Demonstrated

This project demonstrates practical experience in:

- Data Cleaning
- Exploratory Data Analysis
- Feature Engineering
- Business Analytics
- KPI Development
- SQL
- SQLite
- Data Visualization
- Dashboard Development
- Generative AI
- Natural Language Querying
- Business Intelligence
- Anomaly Detection
- Forecasting
- Insight Generation
- Streamlit Application Development

---

## 👩‍💻 Author

### Khushbu Uttam Shelake

**B.Tech CSE (Data Science)**  
JSS Academy of Technical Education, Noida

### Connect With Me

- 💻 GitHub: https://github.com/khushbushelake
- 💼 LinkedIn: https://www.linkedin.com/in/khushbu-uttam-shelake-aaa4b7372
- 🌐 Portfolio: https://my-portfolio-seven-mu-17.vercel.app/

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

**Built with Python, Streamlit, SQL, Business Analytics & Generative AI.**
