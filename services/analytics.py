def get_total_sum(dataframe):
    return sum(row["Сумма"] for row in dataframe)


def get_average_check(dataframe):
    return get_total_sum(dataframe) / len(dataframe) if dataframe else 0


def get_top_3_categories(dataframe):
    category_sum = {}
    for row in dataframe:
        category_sum[row["Категория"]] = (
            category_sum.get(row["Категория"], 0) + row["Сумма"]
        )
    return dict(
        sorted(category_sum.items(), key=lambda item: item[1], reverse=True)[:3]
    )


def get_monthly_analysis(dataframe):
    monthly_sum = {}
    for row in dataframe:
        month = row["Дата"].strftime("%Y-%m")
        monthly_sum[month] = monthly_sum.get(month, 0) + row["Сумма"]
    result = []
    previous_sum = None
    for month, amount in sorted(monthly_sum.items()):
        change = 0 if previous_sum is None else amount - previous_sum
        percent = 0 if previous_sum in (None, 0) else (change / previous_sum) * 100
        result.append(
            {
                "month": month,
                "amount": float(amount),
                "change": float(change),
                "percent": float(percent),
                "status": "↑" if percent > 0 else "↓" if percent < 0 else "→",
            }
        )
        previous_sum = amount
    return result


def build_report(dataframe):
    return {
        "total": round(get_total_sum(dataframe), 2),
        "average": round(get_average_check(dataframe), 2),
        "count": len(dataframe),
        "top3": {
            category: round(amount, 2)
            for category, amount in get_top_3_categories(dataframe).items()
        },
        "monthly": get_monthly_analysis(dataframe),
    }
