# CSV Expense Analysis

Flask-приложение для загрузки CSV с расходами, проверки данных, расчёта метрик и
визуального отчёта. Проект использует стандартную библиотеку Python для CSV и
SVG-графиков, поэтому запускается без бинарных зависимостей NumPy.

![CI](https://github.com/Victor2799/new_project/actions/workflows/tests.yml/badge.svg)

## Установка зависимостей

Установите зависимости в виртуальное окружение:
- Flask
- pytest

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Запуск приложения

Запустите приложение:

```powershell
python app.py
```

Откройте **http://localhost:5000**.

Для production `debug` выключен по умолчанию. Для локальной отладки:

```powershell
$env:FLASK_DEBUG="1"
python app.py
```

## Функционал

### Главная страница (`/`)
- Загрузка CSV с проверкой расширения и MIME-типа
- Проверка колонок `Дата`, `Категория`, `Сумма`
- Отчёт об исключённых строках с номером строки и причиной

### Статистика (`/stats`)
После загрузки файла отображает:
- **Общая сумма** — сумма всех расходов
- **Средний чек** — среднее значение одного расхода
- **Количество записей** — количество строк в данных
- **Топ 3 категории** — категории с максимальными расходами
- **Анализ по месяцам** — расходы по месяцам с процентным изменением относительно предыдущего месяца
- два SVG-графика: расходы по месяцам и топ категорий

Ограничения загрузки:
- только `.csv`;
- разрешённые MIME-типы проверяются на сервере;
- максимальный размер файла — 5 МБ;
- обязательные колонки: `Дата`, `Категория`, `Сумма`;
- неверные суммы, даты, пустые категории и отрицательные значения показываются пользователю и исключаются из отчёта.

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

## Тесты

```powershell
python -m pytest -q
```

GitHub Actions автоматически запускает тесты для каждого push и pull request.

## Структура проекта

```
new_project/
├── app.py                    # Flask приложение и роуты
├── services/
│   ├── csv_service.py        # Чтение и валидация CSV
│   ├── analytics.py          # Расчёты
│   └── charts.py             # Графики в base64
├── tests/
│   └── test_services.py      # Сервисные и Flask-тесты
├── .github/workflows/
│   └── tests.yml             # CI
├── templates/
│   ├── index.html           # Главная страница
│   └── stats.html           # Страница статистики
├── data_pandas.csv           # Пример данных
└── README.md                # Этот файл
```

## Модификация

Для добавления новых метрик создайте функцию в `services/analytics.py` и подключите её в `build_report`.
