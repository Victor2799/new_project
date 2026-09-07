from csv_importer import df


def summa():
    price = sum(df["Сумма"])
    print(f"Общая сумма: {price:.2f}")


def average_check():
    total = sum(df["Сумма"])
    count = len(df)
    avg = total / count
    print(f"Средний чек: {avg:.2f}")


def top_3_categories():
    category_sum = df.groupby("Категория")["Сумма"].sum().sort_values(ascending=False)
    print("\nТоп 3 категории по сумме:")
    for i, (category, amount) in enumerate(category_sum.head(3).items(), 1):
        print(f"{i}. {category}: {amount:.2f}")


def monthly_analysis():
    # Извлекаем месяц (первые 7 символов: YYYY-MM)
    df["Месяц"] = df["Дата"].str[:7]
    
    # Группируем по месяцам и суммируем
    monthly_sum = df.groupby("Месяц")["Сумма"].sum().sort_index()
    
    print("\nАнализ по месяцам:")
    prev_sum = None
    for month, amount in monthly_sum.items():
        if prev_sum is None:
            print(f"{month}: {amount:.2f}")
        else:
            change = amount - prev_sum
            percent = (change / prev_sum) * 100
            status = "↑" if percent > 0 else "↓" if percent < 0 else "→"
            print(f"{month}: {amount:.2f} ({status} {abs(percent):.1f}%)")
        prev_sum = amount


summa()
print(f"Количество записей: {len(df)}")
average_check()
top_3_categories()
monthly_analysis()
