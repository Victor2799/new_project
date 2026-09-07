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
            reader = csv.DictReader(csv_file, strict=True)
            if not reader.fieldnames:
                raise CSVValidationError([{"row": "-", "reason": "CSV-файл пуст."}])
            actual_columns = set(reader.fieldnames)
            missing_columns = REQUIRED_COLUMNS - actual_columns
            extra_columns = actual_columns - REQUIRED_COLUMNS
            if missing_columns or extra_columns:
                reasons = []
                if missing_columns:
                    reasons.append(f"отсутствуют: {', '.join(sorted(missing_columns))}")
                if extra_columns:
                    reasons.append(f"лишние: {', '.join(sorted(extra_columns))}")
                raise CSVValidationError(
                    [
                        {
                            "row": "-",
                            "reason": "Некорректные колонки CSV ("
                            + "; ".join(reasons)
                            + ").",
                        }
                    ]
                )
            rows = list(reader)
    except (UnicodeDecodeError, csv.Error) as error:
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
        if not row.get("Категория", "").strip():
            errors.append(
                {"row": row_number, "reason": "Категория не может быть пустой."}
            )
            row_is_valid = False
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
