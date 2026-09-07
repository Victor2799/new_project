# Flask приложение для анализа расходов

Простое Flask приложение для анализа финансовых данных из CSV файла.

## Установка зависимостей

Установите зависимости:
- Flask
- pandas
- matplotlib
- pytest

```bash
pip install -r requirements.txt
```

## Запуск приложения

1. Откройте терминал в папке проекта
2. Запустите приложение:

```bash
s:/projects/new_project/.venv/Scripts/python.exe app.py
```

3. Откройте браузер и перейдите на: **http://localhost:5000**

## Функционал

### Главная страница (`/`)
- Загрузка CSV с проверкой расширения и MIME-типа
- Проверка колонок `Дата`, `Категория`, `Сумма`
- Отчёт об исключённых строках с номером строки и причиной

### Статистика (`/stats`)
Отображает:
- **Общая сумма** — сумма всех расходов
- **Средний чек** — среднее значение одного расхода
- **Количество записей** — количество строк в данных
- **Топ 3 категории** — категории с максимальными расходами
- **Анализ по месяцам** — расходы по месяцам с процентным изменением относительно предыдущего месяца

### API endpoints

API принимают CSV как multipart-поле `file` методом `POST`.

- `POST /api/total` — общая сумма в JSON
- `POST /api/average` — средний чек в JSON
- `POST /api/top3` — топ 3 категории в JSON
- `POST /api/monthly` — анализ по месяцам в JSON

## Примеры использования API

```bash
# Получить общую сумму
curl -F "file=@data_pandas.csv" http://localhost:5000/api/total

# Получить средний чек
curl -F "file=@data_pandas.csv" http://localhost:5000/api/average

# Получить топ 3 категории
curl -F "file=@data_pandas.csv" http://localhost:5000/api/top3

# Получить анализ по месяцам
curl -F "file=@data_pandas.csv" http://localhost:5000/api/monthly
```

## Структура проекта

```
new_project/
├── app.py                    # Flask приложение и роуты
├── services/
│   ├── csv_service.py        # Чтение и валидация CSV
│   ├── analytics.py          # Расчёты
│   └── charts.py             # Графики в base64
├── tests/
│   └── test_services.py      # Тесты сервисов
├── templates/
│   ├── index.html           # Главная страница
│   └── stats.html           # Страница статистики
├── csv_importer/
│   ├── csv_importer.py      # Загрузка CSV
│   ├── stats.py             # Функции статистики (консольная версия)
│   └── data_pandas.csv      # Данные
└── README.md                # Этот файл
```

## Модификация

Для добавления новых метрик создайте функцию в `services/analytics.py` и подключите её в `build_report`.
