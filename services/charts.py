import base64
from html import escape


def _svg_as_base64(title, values, color):
    width, height = 800, 300
    maximum = max(values.values(), default=1) or 1
    bars = []
    labels = []
    for index, (label, value) in enumerate(values.items()):
        bar_height = int(value / maximum * 210)
        x = 50 + index * max(80, 700 // max(len(values), 1))
        bars.append(
            f'<rect x="{x}" y="{250 - bar_height}" width="45" height="{bar_height}" fill="{color}"/>'
        )
        labels.append(
            f'<text x="{x}" y="275" font-size="12">{escape(str(label))}</text>'
        )
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><text x="20" y="25" font-size="18">{title}</text>{"".join(bars)}{"".join(labels)}</svg>'
    return base64.b64encode(svg.encode("utf-8")).decode("ascii")


def build_charts(dataframe):
    monthly = {}
    categories = {}
    for row in dataframe:
        month = row["Дата"].strftime("%Y-%m")
        monthly[month] = monthly.get(month, 0) + row["Сумма"]
        categories[row["Категория"]] = (
            categories.get(row["Категория"], 0) + row["Сумма"]
        )
    monthly_chart = _svg_as_base64(
        "Расходы по месяцам", dict(sorted(monthly.items())), "#0f766e"
    )
    top_categories = dict(
        sorted(categories.items(), key=lambda item: item[1], reverse=True)[:5]
    )
    category_chart = _svg_as_base64("Топ категорий", top_categories, "#f97316")
    return {"monthly_chart": monthly_chart, "category_chart": category_chart}
