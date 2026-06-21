from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "YRBS_2007.csv"
OUT_TABLES = ROOT / "output" / "tables"
OUT_FIGURES = ROOT / "output" / "figures"
OUT_DATA = ROOT / "data" / "processed"
for p in [OUT_TABLES, OUT_FIGURES, OUT_DATA]:
    p.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW)
cols = ["Sleep", "ComputerUse", "WhatIsYourSex", "InWhatGradeAreYou", "weight", "stratum", "psu"]
clean = df[cols].dropna(subset=["Sleep", "ComputerUse", "WhatIsYourSex", "InWhatGradeAreYou"]).copy()
clean = clean[clean["InWhatGradeAreYou"].isin([1, 2, 3, 4])].copy()

sleep_map = {1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10}
computer_hours_map = {1: 0, 2: 0.5, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5}
computer_label_map = {1: "0 h", 2: "<1 h", 3: "1 h", 4: "2 h", 5: "3 h", 6: "4 h", 7: "5+ h"}
sex_map = {1: "Female", 2: "Male"}
grade_map = {1: "9th", 2: "10th", 3: "11th", 4: "12th"}

clean["sleep_hours_approx"] = clean["Sleep"].astype(int).map(sleep_map)
clean["computer_hours_approx"] = clean["ComputerUse"].astype(int).map(computer_hours_map)
clean["computer_use_label"] = clean["ComputerUse"].astype(int).map(computer_label_map)
clean["sex"] = clean["WhatIsYourSex"].astype(int).map(sex_map)
clean["grade"] = clean["InWhatGradeAreYou"].astype(int).map(grade_map)
clean["sleep_8plus"] = (clean["sleep_hours_approx"] >= 8).astype(int)

order = ["0 h", "<1 h", "1 h", "2 h", "3 h", "4 h", "5+ h"]
clean["computer_use_label"] = pd.Categorical(clean["computer_use_label"], categories=order, ordered=True)
clean.to_csv(OUT_DATA / "yrbs_2007_screen_sleep_cleaned.csv", index=False)

summary = clean.groupby("computer_use_label", observed=False).agg(
    n=("sleep_hours_approx", "size"),
    mean_sleep_hours=("sleep_hours_approx", "mean"),
    sd_sleep_hours=("sleep_hours_approx", "std"),
    se_sleep_hours=("sleep_hours_approx", lambda x: x.std(ddof=1) / np.sqrt(x.count())),
    pct_8plus_sleep=("sleep_8plus", lambda x: 100 * x.mean()),
).reset_index()
summary.to_csv(OUT_TABLES / "group_summary_by_computer_use.csv", index=False)

anova_model = smf.ols("sleep_hours_approx ~ C(computer_use_label)", data=clean).fit()
anova_tbl = anova_lm(anova_model, typ=2)
anova_tbl.to_csv(OUT_TABLES / "anova_sleep_by_computer_use.csv")

reg_model = smf.ols("sleep_hours_approx ~ computer_hours_approx + C(sex) + C(grade)", data=clean).fit(cov_type="HC3")
reg_tbl = pd.DataFrame({
    "term": reg_model.params.index,
    "coef": reg_model.params.values,
    "std_error_HC3": reg_model.bse.values,
    "p_value": reg_model.pvalues.values,
})
reg_tbl.to_csv(OUT_TABLES / "regression_sleep_screen_time.csv", index=False)

# Figures
x = np.arange(len(summary))
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.bar(x, summary["mean_sleep_hours"])
ax.set_xticks(x)
ax.set_xticklabels(summary["computer_use_label"].astype(str))
ax.set_ylabel("Approximate sleep hours")
ax.set_xlabel("Non-school computer / video game use")
ax.set_title("Average sleep hours by recreational screen time")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT_FIGURES / "fig1_mean_sleep_by_screen_time.png", bbox_inches="tight")
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5.2))
ax.plot(x, summary["pct_8plus_sleep"], marker="o")
ax.set_xticks(x)
ax.set_xticklabels(summary["computer_use_label"].astype(str))
ax.set_ylabel("Students sleeping 8+ hours (%)")
ax.set_xlabel("Non-school computer / video game use")
ax.set_title("Share of students getting 8+ hours of sleep")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT_FIGURES / "fig2_pct_8plus_sleep_by_screen_time.png", bbox_inches="tight")
plt.close(fig)

print("Analysis complete.")
print(f"Cleaned sample size: {len(clean):,}")
print(reg_model.summary())
