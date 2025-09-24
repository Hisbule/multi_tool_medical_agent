##Multi-Tool Medical Agent

An AI-powered CLI tool that interacts with medical datasets (heart disease, cancer, diabetes) and performs web-based medical queries.
It is a user interface-based system where you can ask any question in plain English text — no coding required.
If your question is related to data but you don’t mention the dataset name, the system will automatically ask you to choose a database before running the query.
The whole process is fully automatic and interactive..


## PROJECT STRUCTURE

multi-tool-medical-agent/
├─ data/ -> Place original CSV files here: heart.csv, cancer.csv, diabetes.csv
├─ db/ -> Generated SQLite DB files will be saved here
│ ├─ heart_disease.db
│ ├─ cancer.db
│ └─ diabetes.db
├─ src/
│ ├─ convert_csvs.py -> Converts CSVs into SQLite DBs
│ ├─ db_tools.py -> Database tool wrappers
│ ├─ web_search_tool.py -> Web search (SerpAPI / Bing)
│ ├─ agent_main.py -> Main agent CLI interface
│ └─ utils.py -> Helper functions
├─ requirements.txt
├─ README.md
└─ .env.example


##FEATURES

Automatic CSV to SQLite conversion

SQL Query Execution on heart, cancer, and diabetes datasets

Medical Web Search using SerpAPI or Bing

AI Agent Routing between database and web tool

Natural Language Interface (ask questions in plain English)


##EXAMPLE RUN

To run the project, simply run the main Python file: agent_main.py

Question: What's the average age in the dataset?
System: I couldn't determine which DB to use. Please specify: heart/cancer/diabetes
User: heart
Result:
| average_age |
|-------------|
| 54.7        |


##AUTHOR##

Author: Hafiz Uddin Ahmed ADNAN
