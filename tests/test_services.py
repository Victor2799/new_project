from io import BytesIO

import pytest

from app import app
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


def test_load_csv_rejects_extra_columns(tmp_path):
    path = tmp_path / "expenses.csv"
    path.write_text(
        "Дата,Категория,Сумма,Пароль\n2024-01-01,Еда,100,secret\n",
        encoding="utf-8",
    )
    with pytest.raises(CSVValidationError) as error:
        load_csv(path)
    assert "лишние" in error.value.errors[0]["reason"]


def test_load_csv_reports_empty_category(tmp_path):
    path = tmp_path / "expenses.csv"
    path.write_text("Дата,Категория,Сумма\n2024-01-01,,100\n", encoding="utf-8")
    with pytest.raises(CSVValidationError) as error:
        load_csv(path)
    assert "Категория" in error.value.errors[0]["reason"]


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_upload_renders_report_and_charts(client):
    response = client.post(
        "/",
        data={
            "file": (
                BytesIO("Дата,Категория,Сумма\n2024-01-01,Еда,100\n".encode("utf-8")),
                "expenses.csv",
                "text/csv",
            )
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert b"data:image/svg+xml;base64" in response.data
    assert b"100.00" in response.data


def test_api_rejects_invalid_mime_type(client):
    response = client.post(
        "/api/total",
        data={
            "file": (
                BytesIO(b"not an executable"),
                "data.csv",
                "application/octet-stream",
            )
        },
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert "Недопустимый MIME-тип" in response.get_json()["errors"][0]["reason"]
