

import pandas as pd
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DB_DIR = ROOT / "db"
DB_DIR.mkdir(exist_ok=True)


CSV_TO_DB_MAP = {
"heart.csv": "heart_disease.db",
"cancer.csv": "cancer.db",
"diabetes.csv": "diabetes.db",
}




def infer_sqlite_type(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series.dropna()):
        return "INTEGER"
    if pd.api.types.is_float_dtype(series.dropna()):
        return "REAL"
    # Try to detect datetime
    try:
        pd.to_datetime(series.dropna().iloc[:10])
        return "TEXT"
    except Exception:
        return "TEXT"




def dataframe_to_sql(df: pd.DataFrame, conn: sqlite3.Connection, table_name: str):
    # Create table with inferred types, then insert via to_sql
    columns = df.columns
    dtypes = {col: infer_sqlite_type(df[col]) for col in columns}
    col_defs = ", ".join([f'"{c}" {dtypes[c]}' for c in columns])
    create_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({col_defs});'
    cur = conn.cursor()
    cur.execute(create_sql)
    conn.commit()
    # Use pandas to append data (it will coerce types)
    df.to_sql(table_name, conn, if_exists='append', index=False)


if __name__ == "__main__":
    for csv_name, db_name in CSV_TO_DB_MAP.items():
        csv_path = DATA_DIR / csv_name
        if not csv_path.exists():
            print(f"Skipping {csv_name} — file not found in data/ folder")
            continue
        print(f"Processing {csv_name} -> {db_name}")
        df = pd.read_csv(csv_path)
        # Basic cleaning: strip column names
        df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
        conn = sqlite3.connect(DB_DIR / db_name)
        table_name = Path(csv_name).stem
        dataframe_to_sql(df, conn, table_name)
        conn.close()
        print(f"Wrote {db_name} with table {table_name}")