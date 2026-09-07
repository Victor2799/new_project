import pandas as pd
import random
from datetime import timedelta, date

num_rows = 100
start_date = date(2024, 1, 1)
categories = [
    "Продукты",
    "Транспорт",
    "Развлечения",
    "Жильё",
    "Одежда",
    "Техника",
    "Медицина",
]

dates = [
    (start_date + timedelta(days=random.randint(0, 365))).isoformat()
    for _ in range(num_rows)
]
cats = [random.choice(categories) for _ in range(num_rows)]
amounts = [round(random.uniform(50, 15000), 2) for _ in range(num_rows)]

df = pd.DataFrame({"Дата": dates, "Категория": cats, "Сумма": amounts})

df.to_csv("data_pandas.csv", index=False, encoding="utf-8")
print("CSV файл data_pandas.csv создан.")
