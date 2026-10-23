# Sales Performance Analysis — Data Analytics Portfolio Project

**Project type:** Guided, AI-assisted portfolio project  
**Data:** 5,000 rows of synthetic sales transactions generated for practice (not real company data)  
**Tools:** Excel, SQL (SQLite), Python (Pandas), Power BI, Streamlit

## Business problem
A fictional retail company wants to understand sales, profit, product performance, regional trends, and customer segments. The goal is to turn transaction-level data into actionable insights.

## Project deliverables
- `data/sales_data_raw.csv` and `.xlsx`: generated source dataset
- `data/sales_data_cleaned.csv`: cleaned and typed dataset
- `python/clean_data.py`: repeatable cleaning script
- `python/analyze_data.py`: KPI calculations and summary exports
- `sql/sales_analysis.sql`: SQLite table creation and analysis queries
- `app.py`: interactive Streamlit dashboard (code-based dashboard alternative)
- `powerbi/POWER_BI_GUIDE.md`: step-by-step Power BI build guide and DAX measures
- `docs/DATA_DICTIONARY.md`: column definitions
- `docs/PROJECT_CASE_STUDY_TEMPLATE.md`: portfolio case study template

## Quick start (Windows)
1. Extract this ZIP to a folder.
2. Install Python 3.10+ if not already installed.
3. Open Command Prompt or PowerShell in the extracted `Sales_Performance_Analysis` folder.
4. Create a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt:
   ```bat
   .venv\Scripts\activate.bat
   ```
5. Install packages:
   ```powershell
   pip install -r requirements.txt
   ```
6. Run the data analysis:
   ```powershell
   python python\clean_data.py
   python python\analyze_data.py
   ```
7. Launch the code-based dashboard:
   ```powershell
   streamlit run app.py
   ```
   Your browser should open a local dashboard. If not, open the local URL printed in the terminal.

## Power BI
Open Power BI Desktop, choose **Get data → Text/CSV**, and select `data/sales_data_cleaned.csv`. Follow `powerbi/POWER_BI_GUIDE.md` to create measures, charts, slicers and verify the results.

## SQL
The SQL script uses SQLite syntax. It creates a table and runs example queries. To run it:
```powershell
python -c "import sqlite3; c=sqlite3.connect('sales.db'); c.executescript(open('sql/sales_analysis.sql', encoding='utf-8').read()); print('Created sales.db'); c.close()"
```
Then use a SQLite viewer or Python to inspect query outputs. A convenience script is also provided.

## Verification checklist
- Total row count should be 5,000.
- `Order ID` should be unique in this generated dataset.
- `Sales` and `Profit` should be numeric.
- The sum of `Sales` in the Python summary should match Power BI's Total Sales measure.
- The sum of `Profit` in Python should match Power BI's Total Profit measure.
- Filters in each dashboard should change all relevant visuals consistently.

## How to describe AI assistance honestly
You can state: “Used AI tools to support dataset generation, code scaffolding, debugging and documentation; validated calculations and adapted the analysis.” Only claim work you actually understand, ran and verified. Because this dataset is synthetic, do not present its findings as real-world market facts.

## Suggested next steps
1. Run the Python scripts and check their outputs.
2. Build the Power BI report using the guide.
3. Run the Streamlit dashboard.
4. Add screenshots and verified insights to the case study.
5. Upload the project to GitHub after removing temporary files and checking the README.
