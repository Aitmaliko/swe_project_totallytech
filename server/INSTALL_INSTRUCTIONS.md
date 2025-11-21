# Инструкции по установке (Windows)

## Проблема
На Windows без Visual C++ Build Tools некоторые пакеты (psycopg2, httptools) пытаются компилироваться из исходников и зависают.

## Решение 1: Быстрая установка (рекомендуется)

1. Остановите зависшую установку: Ctrl+C
2. Установите зависимости по одной:

```bash
cd server
pip install fastapi==0.109.0
pip install uvicorn==0.27.0
pip install sqlalchemy==2.0.25
pip install psycopg2-binary==2.9.9
pip install pydantic==2.5.3
pip install pydantic-settings==2.1.0
pip install email-validator==2.1.0
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6
pip install aiofiles==23.2.1
```

## Решение 2: Установка всех зависимостей сразу

Используйте флаг --only-binary:

```bash
pip install -r requirements.txt --only-binary :all:
```

Если это не сработает, выполните:

```bash
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

## После установки

Запустите seed_data.py:

```bash
python seed_data.py
```

Затем запустите сервер:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
