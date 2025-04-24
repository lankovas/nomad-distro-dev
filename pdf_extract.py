import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_tables = page.extract_tables()
            for table in extracted_tables:
                df = pd.DataFrame(table)
                df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)  # Clean empty rows/columns
                df.columns = df.iloc[0]  # Set the first row as header
                df = df[1:].reset_index(drop=True)
                tables.append(df)
    
    return tables

# Example usage
pdf_path = "Report.pdf"
tables = extract_tables_from_pdf(pdf_path)

# Display tables
for i, table in enumerate(tables):
    print(f"Table {i+1}:")
    print(table)
    print("\n--------------------\n")