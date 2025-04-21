# REST API веб-сервиса по сбору денежных средств

![](https://img.shields.io/badge/Python-3.9-lightblue)
![](https://img.shields.io/badge/Django-3.2.16-darkgreen)
![](https://img.shields.io/badge/Django_REST_framework-3.12.4-red)

<details>
  <summary>
    Тестовое задание
  </summary>
</details>

### Как запустить проект с помощью docker-контейнеров:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ClosedEyeVisuals/api-donation.git
```

Cоздать .env файл по примеру:
```
SECRET_KEY='sOme_SeCR3t_KeY'
DEBUG=False
ALLOWED_HOSTS=host1, host2
```

Запустить контейнеры:
```
docker compose up
```
Выполнить миграции:

```
docker compose exec backend python manage.py migrate
```

Наполнить БД тестовыми данными

```
docker compose exec backend python manage.py load_collects
```

[Автор](https://github.com/ClosedEyeVisuals)
