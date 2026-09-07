import pytest

from services.analytics import get_monthly_analysis, get_top_3_categories
from services.csv_service import CSVValidationError, load_csv


def test_analytics_and_monthly_change():
    from datetime import datetime

    dataframe = [
        {"Дата": datetime(2024, 1, 1), "Категория": "Еда", "Сумма": 100},
        {"Дата": datetime(2024, 2, 1), "Категория": "Транспорт", "Сумма": 150},
    ]
    assert get_top_3_categories(dataframe) == {"Транспорт": 150, "Еда": 100}
    assert get_monthly_analysis(dataframe)[1]["percent"] == 50


def test_load_csv_skips_invalid_rows(tmp_path):
    path = tmp_path / "expenses.csv"
    path.write_text(
        "Дата,Категория,Сумма\n2024-01-01,Еда,100\ninvalid,Еда,-5\n",
        encoding="utf-8",
    )
    dataframe, errors = load_csv(path)
    assert len(dataframe) == 1
    assert len(errors) == 2


def test_load_csv_rejects_missing_columns(tmp_path):
    path = tmp_path / "expenses.csv"
    path.write_text("Дата,Сумма\n2024-01-01,100\n", encoding="utf-8")
    with pytest.raises(CSVValidationError):
        load_csv(path)
