import os
import tempfile

from flask import Flask, redirect, render_template, request, url_for

from services.analytics import build_report
from services.charts import build_charts
from services.csv_service import CSVValidationError, load_csv

app = Flask(__name__)

ALLOWED_MIME_TYPES = {
    "text/csv",
    "text/plain",
    "application/csv",
    "application/vnd.ms-excel",
}


def process_upload(upload):
    if upload is None or not upload.filename:
        raise CSVValidationError([{"row": "-", "reason": "Выберите CSV-файл."}])
    if not upload.filename.lower().endswith(".csv"):
        raise CSVValidationError(
            [{"row": "-", "reason": "Разрешены только файлы с расширением .csv."}]
        )
    if upload.mimetype not in ALLOWED_MIME_TYPES:
        raise CSVValidationError(
            [{"row": "-", "reason": "Недопустимый MIME-тип файла."}]
        )

    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temporary_file:
            upload.save(temporary_file)
            temporary_path = temporary_file.name
        dataframe, errors = load_csv(temporary_path)
        report = build_report(dataframe)
        report["errors"] = errors
        report.update(build_charts(dataframe))
        return report
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.unlink(temporary_path)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            return render_template(
                "stats.html", **process_upload(request.files.get("file"))
            )
        except CSVValidationError as error:
            return render_template("index.html", errors=error.errors), 400
    return render_template("index.html")


def api_report():
    try:
        return process_upload(request.files.get("file"))
    except CSVValidationError as error:
        return {"errors": error.errors}, 400


@app.route("/api/total", methods=["POST"])
def api_total():
    report = api_report()
    if isinstance(report, tuple):
        return report
    return {"total": report["total"]}


@app.route("/api/average", methods=["POST"])
def api_average():
    report = api_report()
    if isinstance(report, tuple):
        return report
    return {"average": report["average"], "count": report["count"]}


@app.route("/api/top3", methods=["POST"])
def api_top3():
    report = api_report()
    if isinstance(report, tuple):
        return report
    return {
        "categories": [
            {"name": name, "amount": amount} for name, amount in report["top3"].items()
        ]
    }


@app.route("/api/monthly", methods=["POST"])
def api_monthly():
    report = api_report()
    if isinstance(report, tuple):
        return report
    return {"months": report["monthly"]}


@app.route("/stats")
def stats():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
