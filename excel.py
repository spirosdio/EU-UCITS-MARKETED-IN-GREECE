import os
import pandas as pd
import tabula
from pathlib import Path

# Set path to folder with PDFs
pdf_folder = Path("mypath")  # Change if your folder is different
output_csv = "combined_tables.csv"
all_tables = []

for pdf_file in pdf_folder.glob("*.pdf"):
    print(f"Processing {pdf_file.name}")
    try:
        # Extract tables from all pages
        tables = tabula.read_pdf(str(pdf_file), pages='all', multiple_tables=True)
        for table in tables:
            if not table.empty:
                table["Source PDF"] = pdf_file.name
                all_tables.append(table)
    except Exception as e:
        print(f"Failed to read {pdf_file.name}: {e}")

if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_csv(output_csv, index=False)
    print(f"✅ Combined tables saved to: {output_csv}")
else:
    print("⚠️ No tables found.")
