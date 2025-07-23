import os
import pandas as pd
import tabula
from pathlib import Path

# === CONFIGURATION ===
pdf_folder = Path("yourPath")
output_csv = "funds.csv"

# === TABLE AGGREGATION ===
rows = []

for pdf_file in pdf_folder.glob("*.pdf"):
    print(f"Processing: {pdf_file.name}")
    try:
        tables = tabula.read_pdf(str(pdf_file), pages='all', multiple_tables=True)
        fund_name = pdf_file.stem  # filename without extension

        for table in tables:
            if not table.empty:
                for row in table.itertuples(index=False):
                    for cell in row:
                        if isinstance(cell, str) and cell.strip():
                            rows.append([fund_name, cell.strip()])
    except Exception as e:
        print(f"Error with {pdf_file.name}: {e}")

# === SAVE TO CSV ===
df = pd.DataFrame(rows, columns=["Fund", "ETF"])
df.to_csv(output_csv, index=False)
print(f"✅ Saved {len(df)} rows to {output_csv}")
