"""
website_dashboard_generator.py

Creates an interactive website traffic dashboard using Plotly.

Input:
    sample_website_traffic.csv

Output:
    website_traffic_report.html
"""

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Load the website traffic dataset.
# Expected columns: date, page_views, unique_visitors, bounce_rate, traffic_source
df = pd.read_csv("sample_website_traffic.csv")

# Convert date column to datetime format so Plotly can handle time-series charts correctly.
df["date"] = pd.to_datetime(df["date"])

# Aggregate daily metrics for the line chart.
daily_traffic = (
    df.groupby("date", as_index=False)[["page_views", "unique_visitors"]]
    .sum()
)

# Calculate average bounce rate by traffic source for the bar chart.
bounce_by_source = (
    df.groupby("traffic_source", as_index=False)["bounce_rate"]
    .mean()
    .sort_values("bounce_rate", ascending=False)
)

# Calculate total page views by traffic source for the traffic source distribution pie chart.
source_distribution = (
    df.groupby("traffic_source", as_index=False)["page_views"]
    .sum()
)

# Create a line chart showing page views and unique visitors over time.
line_fig = px.line(
    daily_traffic,
    x="date",
    y=["page_views", "unique_visitors"],
    title="Website Traffic Over Time: Page Views vs Unique Visitors",
    labels={
        "date": "Date",
        "value": "Count",
        "variable": "Metric"
    },
    markers=True
)

# Create a bar chart showing average bounce rate by traffic source.
bar_fig = px.bar(
    bounce_by_source,
    x="traffic_source",
    y="bounce_rate",
    title="Average Bounce Rate by Traffic Source",
    labels={
        "traffic_source": "Traffic Source",
        "bounce_rate": "Average Bounce Rate (%)"
    },
    text="bounce_rate"
)
bar_fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")

# Create a pie chart showing distribution of traffic sources based on page views.
pie_fig = px.pie(
    source_distribution,
    names="traffic_source",
    values="page_views",
    title="Traffic Source Distribution by Page Views",
    hole=0.35
)

# Combine all three interactive charts into one HTML report.
# Each chart is embedded as a Plotly HTML block.
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Website Traffic Report</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f7f9fb;
            color: #222;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 10px;
        }}
        p {{
            text-align: center;
            color: #555;
        }}
        .chart {{
            background: white;
            padding: 20px;
            margin: 30px auto;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            max-width: 1100px;
        }}
    </style>
</head>
<body>
    <h1>Website Traffic Report</h1>
    <p>Interactive dashboard showing traffic trends, bounce rate performance, and channel distribution.</p>

    <div class="chart">
        {line_fig.to_html(full_html=False, include_plotlyjs=False)}
    </div>

    <div class="chart">
        {bar_fig.to_html(full_html=False, include_plotlyjs=False)}
    </div>

    <div class="chart">
        {pie_fig.to_html(full_html=False, include_plotlyjs=False)}
    </div>
</body>
</html>
"""

# Save the combined interactive dashboard as a single HTML file.
with open("website_traffic_report.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Dashboard generated successfully: website_traffic_report.html")
