# Документация API проекта Yatube

## Описание

**Yatube** — это социальная платформа для публикации постов, комментариев и взаимодействия с другими пользователями. Проект предоставляет API и позволяет:

- Создавать, читать, обновлять и удалять публикации.
- Добавлять комментарии к публикациям.
- Управлять подписками на других пользователей.
- Получать информацию о сообществах.
- Аутентифицироваться с использованием JWT-токенов.

---

## Установка

Для развертывания проекта на локальной машине выполните следующие шаги:

1. **Клонируйте репозиторий:**
   ```bash
    git clone https://github.com/Kumbbar/api_final_yatube.git
    cd api_final_yatube
    cd yatube-api

    Создайте и активируйте виртуальное окружение:
    python -m venv venv
    source venv/bin/activate  # Для Linux/MacOS
    venv\Scripts\activate     # Для Windows

    Установите зависимости:
    pip install -r requirements.txt

    Примените миграции:
    python manage.py migrate
   
    Запустите сервер:
    python manage.py runserver

API будет доступен по адресу:
http://127.0.0.1:8000/api/v1/

---

## Примеры запросов к API
### Получение списка публикаций

GET /api/v1/posts/?offset=1&limit=1
``` json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": "username",
      "text": "Текст публикации",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "http://example.com/image.jpg",
      "group": 1
    }
  ]
}
```

### Создание новой публикации

POST /api/v1/posts/
``` json
{
  "text": "Новая публикация",
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "group": 1
}
```

Ответ:
``` json
{
  "id": 1,
  "author": "username",
  "text": "Новая публикация",
  "pub_date": "2021-10-14T20:41:29.648Z",
  "image": "http://example.com/image.jpg",
  "group": 1
}
```

### Получение комментариев к публикации

GET /api/v1/posts/1/comments/
``` json

[
  {
    "id": 1,
    "author": "username",
    "text": "Комментарий к публикации",
    "created": "2021-10-14T20:41:29.648Z",
    "post": 1
  }
]
```

### Получение JWT-токена

POST /api/v1/jwt/create/

``` json 
{
  "username": "your_username",
  "password": "your_password"
}
```

Ответ:
``` json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
