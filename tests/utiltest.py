import pandas as pd


def check_df_columns(df_columns: pd.Index, columns: list):
    for col in columns:
        assert col in df_columns, f'column {col} missed in {df_columns}'


def check_all_column_values_in_set(ser_unique: pd._typing.ArrayLike, values: set | list):
    for val in ser_unique:
        assert val in values, f'value {val} is not in list {values[:10]}{"..." if len(values) > 10 else ""}'
