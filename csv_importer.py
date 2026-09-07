# import os
import pandas as pd

# csv_path = os.path.join(os.path.dirname(__file__), "data_pandas.csv")
df = pd.read_csv("data_pandas.csv")


def collec_data_errors(df):
    errors = []
    for index, row in df.iterrows():
        if row.get("Сумма", 0) < 0:
            errors.append({"index": index + 1, "Сумма": row.get("Сумма", 0)})
    return errors


errors = collec_data_errors(df)
