import sqlite3
from pathlib import Path
from typing import List
from tabulate import tabulate


ROOT = Path(__file__).resolve().parents[1]
DB_DIR = ROOT / "db"




class SQLiteDBTool:

	def __init__(self, db_file: str, friendly_name: str):
		self.db_file = DB_DIR / db_file
		self.friendly_name = friendly_name
		if not self.db_file.exists():
			raise FileNotFoundError(f"DB file not found: {self.db_file}")

	def run_sql(self, query: str, max_rows: int = 20) -> str:
		# Very simple - run provided SQL and return tabulated results.
		# WARNING: this executes arbitrary SQL; in production you must sanitize.
		conn = sqlite3.connect(self.db_file)
		cur = conn.cursor()
		try:
			cur.execute(query)
			if cur.description: # it returned rows
				cols = [d[0] for d in cur.description]
				rows = cur.fetchmany(max_rows)
				out = tabulate(rows, headers=cols, tablefmt="github")
				return out
			else:
				conn.commit()
				return "OK"
		except Exception as e:
			return f"SQL Error: {e}"
		finally:
			conn.close()




# Convenience factory functions

def HeartDiseaseDBTool():
	return SQLiteDBTool("heart_disease.db", "Heart Disease DB")

def CancerDBTool():
	return SQLiteDBTool("cancer.db", "Cancer DB")

def DiabetesDBTool():
	return SQLiteDBTool("diabetes.db", "Diabetes DB")