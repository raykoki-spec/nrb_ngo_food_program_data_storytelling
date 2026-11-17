import sqlite3
import pandas as pd

conn = sqlite3.connect("nutrition_program.db")
df = pd.read_csv("nutrition_data.csv")
df.to_sql("nutrition_program", conn, if_exists="replace", index=False)
conn.close()
print("Database ready")