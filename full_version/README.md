# Простое API для сбора и анализа отзывов (полная версия)
## Описание
Это небольшой проект для демонстрации создания API с помощью [FastAPI](https://fastapi.tiangolo.com/) в связке с [SQLAlchemy](https://www.sqlalchemy.org/).
Данная версия проекта имеет правильную иерархическую структуру, имеются возможности конфигурирования и журналирования API.
## Требования
Для работы API требуется использовать Python версии 3.11 и выше.
## Установка
### Linux
```bash
python -m venv venv
venv/bin/pip install .
```
### Windows
```batch
python -m venv venv
venv/Scripts/pip install .
```
## Запуск
### Linux
```bash
./start.sh
```
### Windows
```batch
start.cmd
```
## Демонстрация
1. Пример создания нейтрального отзыва:
    Запрос:
    ```bash
    curl -H "Content-Type: application/json" \
         -d '{"text": "567"}' \
         http://localhost:5001/api/reviews/
    ```
    Ответ:
    ```json
    {
        "id": 13,
        "text": "567",
        "sentiment": "neutral",
        "created_at": "2025-07-17T17:18:09.553968"
    }
    ```
2. Пример создания положительного отзыва:
    Запрос:
    ```bash
    curl -H "Content-Type: application/json" \
         -d '{"text": "тип-топ, очень хорошо"}' \
         http://localhost:5001/api/reviews/
    ```
    Ответ:
    ```json
    {
        "id": 14,
        "text": "тип-топ, очень хорошо",
        "sentiment": "positive",
        "created_at": "2025-07-17T18:16:05.946820"
    }
    ```
3. Пример создания отрицательного отзыва:
    Запрос:
    ```bash
    curl -H "Content-Type: application/json" \
         -d '{"text": "мне не нравится, плохо"}' \
         http://localhost:5001/api/reviews/
    ```
    Ответ:
    ```json
    {
        "id": 15,
        "text": "мне не нравится, плохо",
        "sentiment": "negative",
        "created_at": "2025-07-17T18:20:18.111006"
    }
    ```
4. Пример получения списка положительных отзывов:
    Запрос:
    ```bash
    curl http://localhost:5001/api/reviews/?sentiment=positive
    ```
    Ответ:
    ```json
    [
        {
            "id": 3,
            "text": "оч хорош 123",
            "sentiment": "positive",
            "created_at": "2025-07-17T14:44:05.759023"
        },
        {
            "id": 14,
            "text": "тип-топ, очень хорошо",
            "sentiment": "positive",
            "created_at": "2025-07-17T18:16:05.946820"
        }
    ]
    ```