# Простое API для сбора и анализа отзывов (упрощённая версия)
## Описание
Это небольшой проект для демонстрации создания API с помощью [FastAPI](https://fastapi.tiangolo.com/).
Данная версия проекта состоит лишь из одного модуля.
## Требования
Для работы API требуется использовать Python версии 3.11 и выше.
## Установка
```bash
pip install -r requirements.txt
```
## Запуск
```bash
uvicorn main:app --reload
```
## Демонстрация
1. Пример создания нейтрального отзыва:
    Запрос:
    ```bash
    curl -H "Content-Type: application/json" \
         -d '{"text": "привет!"}' \
         http://localhost:8000/api/reviews/
    ```
    Ответ:
    ```json
    {
        "id": 5,
        "text": "привет!",
        "sentiment": "neutral",
        "created_at": "2025-07-18T10:26:09.080376"
    }
    ```
2. Пример создания положительного отзыва:
    Запрос:
    ```bash
    curl -H "Content-Type: application/json" \
         -d '{"text": "очень, очень люблю это"}' \
         http://localhost:8000/api/reviews/
    ```
    Ответ:
    ```json
    {
        "id": 4,
        "text": "очень, очень люблю это",
        "sentiment": "positive",
        "created_at": "2025-07-18T10:25:52.297893"
    }
    ```
3. Пример создания отрицательного отзыва:
    Запрос:
    ```bash
    curl -H "Content-Type: application/json" \
         -d '{"text": "не нра, ненавижу это"}' \
         http://localhost:8000/api/reviews/
    ```
    Ответ:
    ```json
    {
        "id": 1,
        "text": "не нра, ненавижу это",
        "sentiment": "negative",
        "created_at": "2025-07-18T10:18:56.889195"
    }
    ```
4. Пример получения списка положительных отзывов:
    Запрос:
    ```bash
    curl http://localhost:8000/api/reviews/?sentiment=positive
    ```
    Ответ:
    ```json
    [
      {
        "id": 4,
        "text": "очень, очень люблю это",
        "sentiment": "positive",
        "created_at": "2025-07-18T10:25:52.297893"
      }
    ]
    ```