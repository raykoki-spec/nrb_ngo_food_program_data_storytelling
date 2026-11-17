import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


df = pd.read_csv("nutrition_data.csv")

df["attendance_rate"] = df["sessions_attended"] / (df["months_in_program"] * 4)

df["gain_per_month"] = df["weight_gain_kg"] / df["months_in_program"]

print("Raw:", round(df["sessions_attended"].corr(df["weight_gain_kg"]), 2))
print("Adjusted:", round(df["attendance_rate"].corr(df["gain_per_month"]), 2))

for county, g in df.groupby("county"):
    print(county, round(g["attendance_rate"].corr(g["gain_per_month"]), 2))


"""
FINDINGS:
1 -Kitui county performed best in terms of average weight gain with 0.92
I need a horisontal bar chart with a bar for each county.

2 - Attendance has modest but consistent positive link with weight gain
I need a bar chart and a scatter plot with a trend line to represent this correlation. 

3 - The youngest age group (6 - 12 yrs) gained more weigth than the other 2 groups.
I need a bar chart that shows average weight gain per age group.
"""

"""
HEADLINES

1 - Kitui county is where the program is working the best.

2 - Children who attend more sessions tend to gain more weight.

3 - The youngest age group are the most benefiting from this program.

"""

top_county = df.groupby("county")["weight_gain_kg"].mean().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 4))
colors = ["#1F4E79" if i > 8 else "#AED6F1" for i in range(10)]
top_county.plot(kind="barh", ax=ax, color=colors[::-1])
ax.set_title("Kitui county is where the program is working best.")
ax.set_xlabel("Weight Gain (KG)")
ax.invert_yaxis()
plt.tight_layout()
plt.savefig("best_perfofmong_county.png")


age_group = df.groupby("age_group")["weight_gain_kg"].mean().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#489F26" if i > 8 else "#AED6F1" for i in range(10)]
age_group.plot(kind="bar", ax=ax, color=colors[::-1])
ax.set_title("Youngest participants are benefiting the most")
ax.set_xlabel("Age Group")
ax.bar_label(ax.containers[0], fmt="%.2f kg", padding=3, fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("best_performing_agegroup.png")




analysis = df.dropna(subset=["attendance_rate", "gain_per_month"])

r, p = stats.pearsonr(analysis["attendance_rate"], analysis["gain_per_month"])

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(analysis["attendance_rate"], analysis["gain_per_month"], color="#1F4E79", alpha=0.3, s=30)
slope, intercept = np.polyfit(analysis["attendance_rate"], analysis["gain_per_month"], 1)
x = np.linspace(analysis["attendance_rate"].min(), analysis["attendance_rate"].max(), 100)
ax.plot(x, slope * x + intercept, color="#FF6B6B", linewidth=2)
ax.text(x[-1], slope * x[-1] + intercept + 0.03, "Overall trend", color="red", ha="right", fontsize=11)        
ax.set_title("Children who came to more sessions tend to gain more weight")
ax.set_xlabel("Share of sessions attended")
ax.set_ylabel("Weight gain per month (kg)")
plt.tight_layout()
plt.savefig("attendance_vs_gain.png", dpi=150)