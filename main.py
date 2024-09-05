import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.ticker as ticker


parser = argparse.ArgumentParser(description='Calculate the evolution of the accumulated amount and the contributed capital.')
parser.add_argument('--P', type=float, required=True, help='Initial capital')
parser.add_argument('--r', type=float, required=True, help='Annual interest rate (in decimal)')
parser.add_argument('--M', type=float, required=True, help='Monthly contribution')
parser.add_argument('--n', type=int, required=True, help='Number of compounding periods per year')
parser.add_argument('--t', type=int, required=True, help='Number of years to evaluate')

args = parser.parse_args()

P = int(args.P)
r = float(args.r)/100
M = int(args.M)
n = int(args.n)
t = int(args.t)

fecha_actual = datetime.now()
n_periods = int(t)*int(n)

A = P * (1 + r/n)**(n*t) + M * ((1 + r/n)**(n*t) - 1) / (r/n)
print(f"Approximately {round(A, 2):,} euros in {fecha_actual.year + t}")

vector_dates = [(fecha_actual + relativedelta(months=i)).strftime("%m%Y") for i in range(n_periods)]

vector_contributions = np.full(n_periods, M)
vector_contributions[0] = P
vector_contributions = vector_contributions.tolist()


accumulated_amount_vector = []

for i in range(1, n_periods + 1):
    # Accumulated amount at the end of period i
    A_capital = P * (1 + r / n) ** i
    A_contributions = M * (((1 + r / n) ** i - 1) / (r / n))
    A_total = A_capital + A_contributions
    
    # Total contributed capital by the end of period i
    total_contributed_capital = P + M * i
    
    # Save the data to vectors
    accumulated_amount_vector.append(A_total)

df = pd.DataFrame({"date": vector_dates,
                   "contributions": vector_contributions,
                   "accumulated_amount": accumulated_amount_vector})

df['date'] = pd.to_datetime(df['date'], format="%m%Y").dt.date
df["contributions_t"] = df["contributions"].astype(int)
df = df.sort_values('date', ascending=True)
df['cumulative_contributions'] = df['contributions_t'].cumsum()
df["accumulated_interest"] = df["accumulated_amount"] - df["cumulative_contributions"]

df.to_excel("summary.xlsx", header=True, index=False)

sns.set(style="whitegrid")
plt.figure(figsize=(14, 7))

sns.lineplot(x="date", y="accumulated_amount", data=df, label="Accumulated Wealth")
sns.lineplot(x="date", y="cumulative_contributions", data=df, label="Contributed Capital")
sns.lineplot(x="date", y="accumulated_interest", data=df, label="Accumulated Interest")

plt.title("Evolution of Total Accumulated Wealth, Accumulated Interest and Contributed Capital", fontweight="bold", fontsize=16)
plt.xlabel("Periods")

plt.xticks(rotation=90)
plt.ylabel("Euros")
plt.legend()
plt.tight_layout()

plt.show()
