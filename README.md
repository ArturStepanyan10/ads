# ADS — Платформа для обмена вещами

Это приложение на Django, которое позволяет пользователям размещать объявления и предлагать обмен товарами.

## Установка и запуск

Что необходимо чтоб запустить проект:

- Git
- Docker
- VS Code или PyCharm 
- ЯП Python

### Запуск проекта

#### 1. Клонируйте репозиторий
```bash
git clone https://github.com/ArturStepanyan10/ads
cd ads
```

#### 2. Создайте виртуальное окружение и активируйте его
Windows
```bash
python -m venv venv
cd venv/Scripts
activate
```

MacOS/Linux
```bash
source venv/bin
activate
```

#### 3. Установите зависимости
```bash
pip install -r requirements.txt
```

#### 4. Соберите и запустите контейнеры
```bash
docker-compose up --build
```

#### 5. Применить миграции
```bash
python manage.py migrate
```

#### 6. Запустите проект
```bash
python manage.py runserver
```

