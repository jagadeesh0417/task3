import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 60)
print("EMPLOYEE DATA ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# 1. Load
# ------------------------------------------------------------
print("\n[1] Loading data...")
df = pd.read_csv("data/employees.csv")
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
print(f"Columns: {list(df.columns)}")
print(f"\nFirst 5 rows:\n{df.head().to_string(index=False)}")

# ------------------------------------------------------------
# 2. Initial inspection
# ------------------------------------------------------------
print("\n[2] Initial inspection")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values per column:\n{df.isnull().sum()}")
print(f"\nBasic stats:\n{df.describe(include='all')}")

# ------------------------------------------------------------
# 3. Cleaning
# ------------------------------------------------------------
print("\n[3] Cleaning data...")

# 3a. Drop empty names
before = len(df)
df = df[df["Name"].str.strip() != ""]
print(f"  Removed {before - len(df)} rows with empty names")

# 3b. Parse JoinDate, flag invalid
df["JoinDate"] = pd.to_datetime(df["JoinDate"], errors="coerce")
invalid_dates = df["JoinDate"].isna().sum()
print(f"  Flagged {invalid_dates} invalid JoinDate values as NaT")

# 3c. Fill missing Department with mode
dept_mode = df["Department"].mode()[0]
df["Department"] = df["Department"].fillna(dept_mode)
print(f"  Filled missing Department with mode ('{dept_mode}')")

# 3d. Fill missing numeric values with median
for col in ["Salary", "PerformanceScore"]:
    med = df[col].median()
    df[col] = df[col].fillna(med)
    print(f"  Filled missing {col} with median ({med})")

# 3e. Cap outliers in Salary (beyond 3 std)
mean_sal, std_sal = df["Salary"].mean(), df["Salary"].std()
cap = mean_sal + 3 * std_sal
n_capped = (df["Salary"] > cap).sum()
df["Salary"] = df["Salary"].clip(upper=cap)
print(f"  Capped {n_capped} salary outliers at ${cap:,.0f}")

# 3f. Filter unreasonable Ages (18–65)
df = df[(df["Age"] >= 18) & (df["Age"] <= 65)]
print(f"  Filtered out age outliers (< 18 or > 65)")

print(f"\nCleaned dataset: {len(df)} rows, {len(df.columns)} columns")
print(f"Remaining missing values:\n{df.isnull().sum()}")

# ------------------------------------------------------------
# 4. Filtering
# ------------------------------------------------------------
print("\n[4] Filtering examples")

high_performers = df[df["PerformanceScore"] >= 90]
print(f"  High performers (score >= 90): {len(high_performers)}")

engineers = df[df["Department"] == "Engineering"]
print(f"  Engineering dept: {len(engineers)} employees")

experienced_high = df[(df["YearsExperience"] >= 10) & (df["Salary"] > 80000)]
print(f"  Experienced (>10yr) earning >$80k: {len(experienced_high)}")

# ------------------------------------------------------------
# 5. Grouping & aggregation
# ------------------------------------------------------------
print("\n[5] Grouping & aggregation")

dept_stats = df.groupby("Department").agg(
    EmployeeCount=("EmployeeID", "count"),
    AvgSalary=("Salary", "mean"),
    AvgPerformance=("PerformanceScore", "mean"),
    AvgExperience=("YearsExperience", "mean"),
    AvgAge=("Age", "mean"),
).round(1).sort_values("AvgSalary", ascending=False)
print(f"\nDepartment summary:\n{dept_stats}")

city_stats = df.groupby("City").agg(
    EmployeeCount=("EmployeeID", "count"),
    AvgSalary=("Salary", "mean"),
).round(1).sort_values("AvgSalary", ascending=False)
print(f"\nCity summary (top 5):\n{city_stats.head()}")

# ------------------------------------------------------------
# 6. Insights
# ------------------------------------------------------------
print("\n[6] Key Insights")
print("-" * 40)

best_dept = dept_stats["AvgPerformance"].idxmax()
print(f"1. Best performing dept: {best_dept} ({dept_stats.loc[best_dept, 'AvgPerformance']} avg)")

highest_paid = dept_stats["AvgSalary"].idxmax()
print(f"2. Highest paid dept: {highest_paid} (${dept_stats.loc[highest_paid, 'AvgSalary']:,.0f} avg)")

corr_sal_perf = df["Salary"].corr(df["PerformanceScore"])
print(f"3. Salary vs Performance correlation: {corr_sal_perf:.3f}")

corr_exp_perf = df["YearsExperience"].corr(df["PerformanceScore"])
print(f"4. Experience vs Performance correlation: {corr_exp_perf:.3f}")

avg_tenure = (pd.Timestamp.now() - df["JoinDate"]).dt.days.mean() / 365.25
print(f"5. Average employee tenure: {avg_tenure:.1f} years")

top_city = city_stats["AvgSalary"].idxmax()
print(f"6. Highest avg salary by city: {top_city} (${city_stats.loc[top_city, 'AvgSalary']:,.0f})")

# ------------------------------------------------------------
# 7. Graphs (optional, saved to disk)
# ------------------------------------------------------------
print("\n[7] Generating graphs...")
sns.set_style("whitegrid")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Salary distribution
sns.histplot(df["Salary"], bins=25, kde=True, ax=axes[0, 0])
axes[0, 0].set_title("Salary Distribution")
axes[0, 0].set_xlabel("Salary ($)")

# Performance by department
sns.boxplot(data=df, x="Department", y="PerformanceScore", ax=axes[0, 1])
axes[0, 1].set_title("Performance Score by Department")
axes[0, 1].tick_params(axis="x", rotation=45)

# Avg salary by department
dept_stats["AvgSalary"].plot(kind="bar", ax=axes[1, 0], color="steelblue")
axes[1, 0].set_title("Average Salary by Department")
axes[1, 0].set_ylabel("Avg Salary ($)")
axes[1, 0].tick_params(axis="x", rotation=45)

# Experience vs Performance scatter
sns.scatterplot(data=df, x="YearsExperience", y="PerformanceScore", hue="Department", alpha=0.6, ax=axes[1, 1])
axes[1, 1].set_title("Experience vs Performance")
axes[1, 1].legend(bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.savefig("data/analysis_plots.png", dpi=150, bbox_inches="tight")
print("  Saved plots to data/analysis_plots.png")
plt.close()
print("\nDone!")
