import pandas as pd
import pdfplumber
import os


def parse_file(file_path):
    # """Parse Excel, CSV, or PDF files."""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == ".csv":
        df = pd.read_csv(file_path)
        text = df.to_string()
    elif file_extension == ".xlsx":
        df = pd.read_excel(file_path)
        text = df.to_string()
    elif file_extension == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            tables = []
            for page in pdf.pages:
                page_tables = page.extract_tables()
                for table in page_tables:
                    try:
                        tables.append(pd.DataFrame(table[1:], columns=table[0]))
                    except Exception:
                        pass  # Skip malformed tables
            if tables:
                try:
                    df = pd.concat(tables, ignore_index=True)
                except ValueError:
                    df = tables[0]  # Fallback to first table if concat fails
            else:
                df = pd.DataFrame({"text": [text]})
    else:
        raise ValueError("Unsupported file format")
    
    return df, text


# def parse_file(file_path):
#     """Parse Excel, CSV, or PDF files."""
#     file_extension = os.path.splitext(file_path)[1].lower()

#     if file_extension == ".csv":
#         df = pd.read_csv(file_path)
#         text = df.to_string()
#     elif file_extension == ".xlsx":
#         df = pd.read_excel(file_path)
#         text = df.to_string()
#     elif file_extension == ".pdf":
#         with pdfplumber.open(file_path) as pdf:
#             text = "

# ".join([page.extract_text() or "" for page in pdf.pages])
#             tables = []
#             for page in pdf.pages:
#                 page_tables = page.extract_tables()
#                 for table in page_tables:
#                     try:
#                         tables.append(pd.DataFrame(table[1:], columns=table[0]))
#                     except Exception:
#                         pass  # Skip malformed tables
#             if tables:
#                 try:
#                     df = pd.concat(tables, ignore_index=True)
#                 except ValueError:
#                     df = tables[0]  # Fallback to first table if concat fails
#             else:
#                 df = pd.DataFrame({"text": [text]})
#     else:
#         raise ValueError("Unsupported file format")

    return df, text
