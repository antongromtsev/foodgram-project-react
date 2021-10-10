![main.yml](https://github.com/antongromtsev/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# foodgram-project-react
Приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. Документация по работе с API после развертывания и настройки проекта будет доступна по адресу: http://127.0.0.1/api/docs
## Перед запуском проекта
Инструкции помогут вам развернуть и запустить копию проекта на вашем сервер для целей разработки и тестирования. Примечания о том, как развернуть проект в действующей системе, см. в разделе "Развертывание проекта".
### Необходимое окружение
Чтобы запустить проект, вам необходимо на серверной машине установить Docker (docker.io, docker-compose). Загрузите эту программу с официального [веб-сайта](https://www.docker.com/)
Инструкция по утановке [Docker Linux](https://docs.docker.com/engine/install/ubuntu/)

## Развёртывание проекта
1. Клонировать репозиторий на локальный компьютер с [github](https://github.com/): 
```bash
git clone https://github.com/antongromtsev/foodgram-project-react.git
```
2. На сайте github.com в директории проекта перейдите на вкладку "Settings"
3. Выберите вкладку "Secrets"
4. Добавьте переменные среды:
    1. Доступ к Docker Hub:
        * DOCKER_USER - имя пользователя
        * DOCKER_PASSWORD - пароль
    2. Доступ на сервер, где будет развернут проект:
        * HOST_SERVER - адрес сервера
        * USER_SERVER - имя пользователя
        * SERVER_SSH_KEY - ключ для доступа по ssh
        * PASSPHRASE - секретное слово (необходимо указать, если используется)
        * Ключ-ssh находиться в папке пользователя в файле .ssh/id_rsa *
    3. Переменные окружения для конфигурации БД:
        * DB_NAME=postgres - имя базы данных
        * POSTGRES_USER=xxxxxx - логин для подключения к базе данных (установите свой)
        * POSTGRES_PASSWORD=xxxxxxx - пароль для подключения к БД (установите свой)
        * DB_HOST=db - название сервиса (контейнера)
        * DB_PORT=5432 - порт для подключения к БД
5. Скопируйте файл "nginx_deploy.conf" с файлами конфигурации и файл с инструкциями для docker-compose "docker-compose_deploy.yaml" на сервер и убрать суфикс "_deploy" из названия.
*для этого можно воспользоваться командой [scp](https://losst.ru/kopirovanie-fajlov-scp)*
6. В настройка settings.py укажите адрес сервера 
    *Пример* ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'web', '84.201.136.198']
7. Сделайте push на github.
```bash
git push
```  
После push проекта на github будет запущено:
    * Проверка на соответствие PEP8
    * Создание образа и отправка его на сервер Docker Hub
    * Загрузка образа на серверб развертывание и запуск
## Настройка проекта
1. Откройте консоль, перейти в директорию проекта и создайте супер пользователя:
```bash
docker exec -it <имя_пользователя>_web_1 python manage.py createsuperuser
```
Следуйте инструкции в консоли.

2. При необходимости БД можно заполнить тестовыми данными
```bash
docker exec -it <имя_пользователя>_web_1 python manage.py loaddata dump_ingredient.json (dump_tag.json)
```
*Предварительно необходимо скопировать файлы "dump_ingredient.json", "dump_tag.json" из папки "backend/foodgram" на сервер*

После завершения настройки проект будет запущен и доступен по адресу: http://HOST_SERVER/

Образ на Docker Hub находиться по адресу:
https://hub.docker.com/repository/docker/fenix217grom/foodgram-backend,
https://hub.docker.com/repository/docker/fenix217grom/foodgram-frontend

# Проект доступен по адресу:

foodgram-project-react: http://84.201.136.198

### Логин и пароль для входа от имени администратора:

```
email: f@g.com
password: admin
```
