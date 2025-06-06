# -*- coding: utf-8 -*-
"""Task 3 (Weather report generator and pdf generator ).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pPE-HKnG_aRxoax2lzVF9opFbB3kenWp
"""

# 📦 Install all required packages
!pip install requests pandas matplotlib seaborn fpdf

import requests
import pandas as pd

import requests
import pandas as pd

# Bengaluru weather request
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 12.97,
    "longitude": 77.59,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "windspeed_10m_max"
    ],
    "timezone": "Asia/Kolkata"
}

# Fetch and parse
response = requests.get(url, params=params)
data = response.json()

# Create DataFrame
df = pd.DataFrame({
    "date": data["daily"]["time"],
    "temp_max": data["daily"]["temperature_2m_max"],
    "temp_min": data["daily"]["temperature_2m_min"],
    "precipitation": data["daily"]["precipitation_sum"],
    "wind_speed": data["daily"]["windspeed_10m_max"]
})

# Convert to datetime
df["date"] = pd.to_datetime(df["date"])

# Preview
df.head()

import matplotlib.pyplot as plt
import seaborn as sns

# Clean theme for seaborn
sns.set(style="whitegrid")
df["month"] = df["date"].dt.month

plt.figure(figsize=(14, 5))
plt.plot(df["date"], df["temp_max"], label="Max Temp", color="tomato")
plt.plot(df["date"], df["temp_min"], label="Min Temp", color="skyblue")
plt.title("🌡️ Daily Max & Min Temperatures in Bangalore (2024)", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.tight_layout()
plt.show()

monthly_rain = df.groupby("month")["precipitation"].mean().reset_index()

plt.figure(figsize=(10, 5))
sns.barplot(x="month", y="precipitation", data=monthly_rain, palette="Blues_d")
plt.title("🌧️ Average Monthly Rainfall in Bangalore (2024)", fontsize=16)
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="month", y="wind_speed", data=df, palette="pastel")
plt.title("🍃 Monthly Wind Speed Distribution in Bangalore (2024)", fontsize=16)
plt.xlabel("Month")
plt.ylabel("Wind Speed (km/h)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
sns.histplot(df["temp_max"], bins=20, color="orange", kde=True)
plt.title("📊 Distribution of Max Daily Temperatures in Bangalore (2024)", fontsize=16)
plt.xlabel("Max Temperature (°C)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Ensure 'date' column is datetime
df["date"] = pd.to_datetime(df["date"])

# Get user input
input_date = input("📅 Enter a date (YYYY-MM-DD): ")

# Try converting and searching
try:
    user_date = pd.to_datetime(input_date)
    result = df[df["date"] == user_date]

    if not result.empty:
        row = result.iloc[0]
        print(f"\n📍 Weather on {user_date.date()} in Bangalore:")
        print(f"🌡️ Max Temp: {row['temp_max']} °C")
        print(f"❄️ Min Temp: {row['temp_min']} °C")
        print(f"🌧️ Rainfall: {row['precipitation']} mm")
        print(f"🍃 Wind Speed: {row['wind_speed']} km/h")
    else:
        print("⚠️ No weather data available for that date.")
except Exception as e:
    print("❌ Invalid date format. Please enter it as YYYY-MM-DD.")

!pip install fpdf

plt.figure(figsize=(12, 5))
plt.plot(df["date"], df["temp_max"], label="Max Temp", color="tomato")
plt.plot(df["date"], df["temp_min"], label="Min Temp", color="skyblue")
plt.title("🌡️ Daily Max and Min Temperatures in Bangalore (2024)", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.tight_layout()
plt.savefig("temp_plot.png")  # ✅ Save
plt.show()

monthly_rain = df.groupby("month")["precipitation"].mean().reset_index()

plt.figure(figsize=(10, 5))
sns.barplot(x="month", y="precipitation", data=monthly_rain, palette="Blues_d")
plt.title("🌧️ Average Monthly Rainfall in Bangalore (2024)", fontsize=16)
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.tight_layout()
plt.savefig("rain_plot.png")  # ✅ Save
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="month", y="wind_speed", data=df, palette="pastel")
plt.title("🍃 Monthly Wind Speed Distribution in Bangalore (2024)", fontsize=16)
plt.xlabel("Month")
plt.ylabel("Wind Speed (km/h)")
plt.tight_layout()
plt.savefig("wind_plot.png")  # ✅ Save
plt.show()

plt.figure(figsize=(10, 5))
sns.histplot(df["temp_max"], bins=20, color="orange", kde=True)
plt.title("📊 Distribution of Max Daily Temperatures in Bangalore (2024)", fontsize=16)
plt.xlabel("Max Temperature (°C)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("hist_plot.png")  # ✅ Save
plt.show()

from fpdf import FPDF
import datetime

# Summary statistics
avg_max_temp = round(df["temp_max"].mean(), 2)
avg_min_temp = round(df["temp_min"].mean(), 2)
total_rainfall = round(df["precipitation"].sum(), 2)
avg_wind = round(df["wind_speed"].mean(), 2)

# Ask user for a date
user_input = input("📅 Enter a date (YYYY-MM-DD) to include in the report: ")
try:
    user_date = pd.to_datetime(user_input, dayfirst=True)
    row = df[df["date"] == user_date].iloc[0]
    user_weather = {
        "Date": str(user_date.date()),
        "Max Temp": f"{row['temp_max']} °C",
        "Min Temp": f"{row['temp_min']} °C",
        "Rainfall": f"{row['precipitation']} mm",
        "Wind Speed": f"{row['wind_speed']} km/h"
    }
except:
    user_weather = {
        "Date": user_input,
        "Error": "No data found for this date."
    }

# Initialize PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Title Page
pdf.add_page()
pdf.set_font("Arial", 'B', 20)
pdf.cell(0, 10, "Climate Trends - Bangalore (2024)", ln=True, align="C")
pdf.ln(10)
pdf.set_font("Arial", '', 14)
pdf.cell(0, 10, f"Generated on: {datetime.date.today()}", ln=True, align="C")

# Summary Section
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, "Weather Summary (Jan to Dec 2024)", ln=True)
pdf.ln(5)

pdf.set_font("Arial", '', 12)
pdf.cell(0, 10, f"Average Max Temp: {avg_max_temp} °C", ln=True)
pdf.cell(0, 10, f"Average Min Temp: {avg_min_temp} °C", ln=True)
pdf.cell(0, 10, f"Total Rainfall: {total_rainfall} mm", ln=True)
pdf.cell(0, 10, f"Average Wind Speed: {avg_wind} km/h", ln=True)

# User-Specified Weather
pdf.ln(10)
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "User-Requested Weather Info:", ln=True)
pdf.set_font("Arial", '', 12)
for k, v in user_weather.items():
    pdf.cell(0, 10, f"{k}: {v}", ln=True)

# Add Plots
plots = ["temp_plot.png", "rain_plot.png", "wind_plot.png", "hist_plot.png"]
for plot in plots:
    try:
        pdf.add_page()
        pdf.image(plot, x=10, y=30, w=180)
    except:
        pdf.cell(0, 10, f"Could not load {plot}", ln=True)

# Save PDF
pdf.output("Climate_Report_Bangalore_2024.pdf")
print("✅ PDF report saved as 'Climate_Report_Bangalore_2024.pdf'")