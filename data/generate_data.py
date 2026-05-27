import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

n = 200
data = {
    "EmployeeID": [f"EMP{i:03d}" for i in range(1, n+1)],
    "Name": [f"Employee_{i}" for i in range(1, n+1)],
    "Age": np.random.randint(22, 65, n).tolist(),
    "Department": np.random.choice(
        ["Engineering", "Marketing", "Sales", "HR", "Finance", "Support"],
        n, p=[0.25, 0.15, 0.20, 0.10, 0.15, 0.15]
    ).tolist(),
    "Salary": np.random.normal(70000, 20000, n).round(-3).astype(int).tolist(),
    "YearsExperience": np.random.randint(0, 35, n).tolist(),
    "PerformanceScore": np.clip(np.random.normal(75, 12, n).round(1), 0, 100).tolist(),
    "JoinDate": [
        (datetime(2015, 1, 1) + timedelta(days=int(np.random.randint(0, 3650)))).strftime("%Y-%m-%d")
        for _ in range(n)
    ],
    "City": np.random.choice(
        ["New York", "San Francisco", "Chicago", "Austin", "Seattle", "Boston", "Denver"],
        n
    ).tolist(),
}

df = pd.DataFrame(data)

na_idx = np.random.choice(df.index, 15, replace=False)
df.loc[na_idx, "Salary"] = np.nan
na_idx2 = np.random.choice(df.index, 10, replace=False)
df.loc[na_idx2, "PerformanceScore"] = np.nan
na_idx3 = np.random.choice(df.index, 8, replace=False)
df.loc[na_idx3, "Department"] = np.nan

outlier_idx = np.random.choice(df.index, 3, replace=False)
df.loc[outlier_idx, "Salary"] = [250000, 300000, 500000]
outlier_idx2 = np.random.choice(df.index, 2, replace=False)
df.loc[outlier_idx2, "Age"] = [18, 70]

df.loc[df.sample(5).index, "JoinDate"] = "invalid-date"
df.loc[df.sample(3).index, "Name"] = ""

df.to_csv("data/employees.csv", index=False)
print("employees.csv created with", len(df), "rows")
