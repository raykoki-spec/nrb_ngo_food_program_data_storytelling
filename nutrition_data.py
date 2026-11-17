"""
Generate realistic sample data for a nutrition program run by a Nairobi NGO
across three counties. Output: nutrition_program_outcomes.csv

Columns: participant_id, county, age_group, weight_gain_kg,
         sessions_attended, months_in_program

Patterns built in (so the exercise has real stories to find):
  1. County performance differs (Kisumu > Machakos > Turkana)
  2. More sessions attended -> more weight gain (with plenty of noise)
  3. Age groups respond differently (youngest children gain the most)
"""

import numpy as np
import pandas as pd

SEED = 42
N = 600
rng = np.random.default_rng(SEED)

# ---- Program setup ---------------------------------------------------------
counties = {
    # share of participants, avg attendance rate (Beta params), county effect
    "Kitui":   {"share": 0.35, "att": (8, 2.5), "effect": 1.15},
    "Machakos": {"share": 0.35, "att": (6, 3.0), "effect": 1.00},
    "Laikipia":  {"share": 0.30, "att": (4, 3.5), "effect": 0.85},  # drought, long distances
}

age_groups = {
    # share, monthly weight gain (kg) at full attendance
    "6-12 years": {"share": 0.35, "rate": 0.25},
    "13-18 years": {"share": 0.40, "rate": 0.17},
    "19-35 years":  {"share": 0.25, "rate": 0.12},
}

SESSIONS_PER_MONTH = 4  # weekly sessions

# ---- Generate participants -------------------------------------------------
county_names = list(counties)
county_draw = rng.choice(
    county_names, size=N, p=[counties[c]["share"] for c in county_names]
)

age_names = list(age_groups)
age_draw = rng.choice(
    age_names, size=N, p=[age_groups[a]["share"] for a in age_names]
)

# Most participants have completed 6 months; some joined later
months = rng.choice([3, 4, 5, 6], size=N, p=[0.10, 0.15, 0.20, 0.55])

rows = []
for i in range(N):
    county, age, m = county_draw[i], age_draw[i], months[i]

    # Attendance rate for this participant, driven by county
    a, b = counties[county]["att"]
    attendance_rate = rng.beta(a, b)
    max_sessions = m * SESSIONS_PER_MONTH
    sessions = int(round(attendance_rate * max_sessions))
    sessions = min(max(sessions, 0), max_sessions)

    # Weight gain: age-group rate x months x county effect x attendance factor
    attendance_factor = 0.35 + 0.65 * (sessions / max_sessions)
    expected = (
        age_groups[age]["rate"] * m * counties[county]["effect"] * attendance_factor
    )
    gain = expected + rng.normal(0, 0.25)  # individual variation
    gain = round(float(np.clip(gain, -0.5, None)), 2)  # a few may lose weight

    rows.append(
        {
            "participant_id": f"NP{i + 1:04d}",
            "county": county,
            "age_group": age,
            "weight_gain_kg": gain,
            "sessions_attended": sessions,
            "months_in_program": int(m),
        }
    )

df = pd.DataFrame(rows)
df.to_csv("nutrition_program_outcomes.csv", index=False)

# ---- Quick sanity check ----------------------------------------------------
print(f"Saved {len(df)} rows to nutrition_program_outcomes.csv\n")
print(df.head(), "\n")
print("Avg weight gain by county:\n", df.groupby("county")["weight_gain_kg"].mean().round(2), "\n")
print("Avg weight gain by age group:\n", df.groupby("age_group")["weight_gain_kg"].mean().round(2), "\n")
print("Correlation (sessions vs weight gain):",
      round(df["sessions_attended"].corr(df["weight_gain_kg"]), 2))
