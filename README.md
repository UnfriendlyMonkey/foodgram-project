# Личный проект Foodgram
[адрес на github](https://github.com/andreysereda1976/foodgram-project)

![foodgram_workflow](https://github.com/andreysereda1976/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)

[Проект временно запущен по адресу: http://84.201.166.64/](http://84.201.166.64/)
[и ummy.online](http://ummy.online/)

- Студент: Андрей Середа (10 когорта).
- Ревьюер: Станислав Лосев.

 *Дипломный проект в рамках обучения в Яндекс.Практикум по профессии Python-разработчик*

---
 Проект представляет собой ....

---

### Памятка

#### 1. Сборка проекта

выполните команды ```docker-compose build``` для сборки проекта и ```docker-compose up``` для его запуска

#### 2. Миграции
для создания и завершения миграций, а также предзаполнения вспомогательных БД выполните команды
```

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py load_ingredients
docker-compose exec web python manage.py fill_tags
```
(проект работает на PostgreSQL)

#### 3. Создание суперпользователя
Суперпользователь с доступом к административной части проекта может быть создан командой
```
docker-compose exec web python manage.py createsuperuser
```

#### 4. Сбор статики
Статика в проекте раздается через Nginx. Для ее сбора выполните команду
```
docker-compose exec web python manage.py collectstatic --no-input
```

#### 5. Значения из переменных окружения
Общие значения в файле settings.py, относящиеся к подключению и работой с БД, такие как:
```
        'default': {
            'ENGINE': # указание, с каким типом БД работаем,
            'NAME': # имя БД,
            'USER': # логин для подключения к базе данных,
            'PASSWORD': # пароль для подключения к БД,
            'HOST': # название сервиса (контейнера),
            'PORT': # порт для подключения к БД,
        }
```
Будут загружаться из переменных окружения.
