import pandas as pd
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, Inserter, TableDefinition, SqlType, TableName

def export_to_powerbi(df, output_path):
    """Export DataFrame to CSV for PowerBI."""
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

    # Map pandas dtypes to Tableau SqlType
    def get_sql_type(dtype):
        if pd.api.types.is_integer_dtype(dtype):
            return SqlType.big_int()
        elif pd.api.types.is_float_dtype(dtype):
            return SqlType.double()
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return SqlType.date()
        elif pd.api.types.is_bool_dtype(dtype):
            return SqlType.bool()
        else:
            return SqlType.text()

    try:
        with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(endpoint=hyper.endpoint, database=output_path, create_mode=CreateMode.CREATE_AND_REPLACE) as connection:
                table_def = TableDefinition(table_name=TableName("Extract", "Extract"))
                for col in df.columns:
                    dtype = df[col].dtype
                    table_def.add_column(str(col), get_sql_type(dtype))

                connection.catalog.create_table(table_definition=table_def)

                with Inserter(connection, table_def) as inserter:
                    for _, row in df.iterrows():
                        inserter.add_row(row.tolist())
                    inserter.execute()
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to export to Tableau .hyper file: {str(e)}")
