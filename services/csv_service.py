import csv
from datetime import datetime

REQUIRED_COLUMNS = {"Дата", "Категория", "Сумма"}


class CSVValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__("CSV validation failed")


def load_csv(path):
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            if not reader.fieldnames:
                raise CSVValidationError([{"row": "-", "reason": "CSV-файл пуст."}])
            missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)
            if missing_columns:
                missing = ", ".join(sorted(missing_columns))
                raise CSVValidationError(
                    [
                        {
                            "row": "-",
                            "reason": f"Отсутствуют обязательные колонки: {missing}.",
                        }
                    ]
                )
            rows = list(reader)
    except UnicodeDecodeError as error:
        raise CSVValidationError(
            [
                {
                    "row": "-",
                    "reason": "Не удалось разобрать CSV. Проверьте разделитель и кодировку.",
                }
            ]
        ) from error
    errors = []
    valid_rows = []
    for row_number, row in enumerate(rows, start=2):
        row_is_valid = True
        try:
            amount = float(row["Сумма"])
        except (TypeError, ValueError):
            errors.append({"row": row_number, "reason": "Сумма не является числом."})
            row_is_valid = False
            amount = 0
        if amount < 0:
            errors.append(
                {"row": row_number, "reason": "Отрицательная сумма пропущена."}
            )
            row_is_valid = False
        try:
            date = datetime.fromisoformat(row["Дата"])
        except (TypeError, ValueError):
            errors.append({"row": row_number, "reason": "Дата имеет неверный формат."})
            row_is_valid = False
            date = None
        if not row_is_valid:
            continue
        valid_rows.append(
            {"Дата": date, "Категория": row["Категория"], "Сумма": amount}
        )

    if not valid_rows:
        raise CSVValidationError(
            errors or [{"row": "-", "reason": "В CSV нет корректных строк."}]
        )
    return valid_rows, errors
