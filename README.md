# testwork_back
Тестовое задание для вакансии на бекенд-разработчика

Установка и Запуск
=====================
Воспользоваться приложением можно вручную или при помощи Docker'а

- **Docker**
1. Выполнить сборку контейнера `docker build . -t testwork`
2. Запустить контейнер `docker run -p 8080:8080 testwork`

- **Python**
1. Установить python 3.11
2. Создать виртуальное окружение `python -m venv`
3. Установить необходимые библиотеки выполнив `pip install -r requirements.txt`
4. Запустить приложение командой `python -m main`

Настройка
==========================
При необходимости можно изменить путь к хранилищу `storage_path` и порт `port` 
в файле конфигурации `config.yml`.

Эксплуатация
==========================
Для тестирования функций приложения можно открыть ссылку http://localhost:8080/docs .
Там доступен встроенный интерфейс FastAPI для этих целей.

**Доступные функции**
- Создание файла (или замена с обновлением, если он уже существует) `Create Upload File`
- Обновление файла (если он существует) `Update File`
- Обновление информации о файлах в храниелище в БД `Actualize`
- Загрузка файла (если он существует) `Download File`
- Получение информации обо всех файлах в хранилище `Get All`
- Получение информации о конкретном файле по его пути в хранилище `Get`
- Удаление файла (если он существует) `Delete`
- Поиск файла по части пути и названия `Search`