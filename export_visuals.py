# import pandas as pd
# from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, Inserter, TableDefinition, SqlType, TableName

# def export_to_powerbi(df, output_path):
#     """Export DataFrame to CSV for PowerBI."""
#     if df.empty or not df.columns.any():
#         raise ValueError("DataFrame is empty or has no columns.")
#     try:
#         df.to_csv(output_path, index=False)
#         return output_path
#     except Exception as e:
#         raise RuntimeError(f"Failed to export to CSV: {str(e)}")

# def export_to_tableau(df, output_path):
#     """Export DataFrame to Tableau .hyper file with dynamic type mapping."""
#     if df.empty or not df.columns.any():
#         raise ValueError("DataFrame is empty or has no columns.")

#     # Map pandas dtypes to Tableau SqlType
#     def get_sql_type(dtype):
#         if pd.api.types.is_integer_dtype(dtype):
#             return SqlType.big_int()
#         elif pd.api.types.is_float_dtype(dtype):
#             return SqlType.double()
#         elif pd.api.types.is_datetime64_any_dtype(dtype):
#             return SqlType.date()
#         elif pd.api.types.is_bool_dtype(dtype):
#             return SqlType.bool()
#         else:
#             return SqlType.text()

#     try:
#         with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
#             with Connection(endpoint=hyper.endpoint, database=output_path, create_mode=CreateMode.CREATE_AND_REPLACE) as connection:
#                 table_def = TableDefinition(table_name=TableName("Extract", "Extract"))
#                 for col in df.columns:
#                     dtype = df[col].dtype
#                     table_def.add_column(str(col), get_sql_type(dtype))

#                 connection.catalog.create_table(table_definition=table_def)

#                 with Inserter(connection, table_def) as inserter:
#                     for _, row in df.iterrows():
#                         inserter.add_row(row.tolist())
#                     inserter.execute()
#         return output_path
#     except Exception as e:
#         raise RuntimeError(f"Failed to export to Tableau .hyper file: {str(e)}")


import pandas as pd
from tableauhyperapi import (
    HyperProcess, Telemetry, Connection, CreateMode,
    Inserter, TableDefinition, SqlType, TableName, NOT_NULLABLE, NULLABLE
)

def export_to_powerbi(df, output_path):
    # """Export DataFrame to CSV for PowerBI."""
    if df.empty or not df.columns.any():
        raise ValueError("DataFrame is empty or has no columns.")
    try:
        df.to_csv(output_path, index=False)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to export to CSV: {str(e)}")

def export_to_tableau(df, output_path):
    """Export DataFrame to Tableau .hyper file with dynamic type mapping."""
    if df.empty or not df.columns.any():
        raise ValueError("DataFrame is empty or has no columns.")

    def get_sql_type(dtype):
        if pd.api.types.is_integer_dtype(dtype):
            return SqlType.big_int()
        elif pd.api.types.is_float_dtype(dtype):
            return SqlType.double()
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return SqlType.timestamp()
        elif pd.api.types.is_bool_dtype(dtype):
            return SqlType.bool()
        else:
            return SqlType.text()

    # Build table definition for Extract.Extract
    extract_table = TableDefinition(
        table_name=TableName("Extract", "Extract"),
        columns=[
            TableDefinition.Column(
                name=str(col),
                type=get_sql_type(df[col].dtype),
                nullability=NULLABLE
            )
            for col in df.columns
        ]
    )

    try:
        with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(
                endpoint=hyper.endpoint,
                database=output_path,
                create_mode=CreateMode.CREATE_AND_REPLACE
            ) as connection:
                # Ensure schema + table exist
                connection.catalog.create_schema(schema=extract_table.table_name.schema_name)
                connection.catalog.create_table(table_definition=extract_table)

                # Coerce to python-native values
                clean_df = df.copy()
                # Convert datetimes to Python datetime (Hyper expects python-native objects)
                for c in clean_df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns:
                    clean_df[c] = pd.to_datetime(clean_df[c], errors="coerce")
                # Replace pandas NA with None
                clean_df = clean_df.where(pd.notnull(clean_df), None)

                # Insert rows using Inserter
                with Inserter(connection, extract_table) as inserter:
                    inserter.add_rows(rows=[tuple(row) for row in clean_df.itertuples(index=False, name=None)])
                    inserter.execute()

        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to export to Tableau .hyper file: {str(e)}")
