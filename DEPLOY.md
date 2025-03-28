# Инструкция по деплою Perfecto в production

Эта инструкция описывает шаги по деплою Perfecto в production-среду с использованием Docker, Docker Compose и GitHub Actions.

## Предварительные требования

1. Сервер с Docker и Docker Compose
2. Доступ по SSH к серверу
3. Настроенный домен, указывающий на сервер
4. GitHub-репозиторий проекта

## Подготовка переменных окружения

1. Создайте файл `.env.prod` на основе примера:
   ```bash
   cp .env.prod.example .env.prod
   ```

2. Сгенерируйте надежный секретный ключ Django:
   ```bash
   python generate_secret_key.py .env.prod
   ```

3. Отредактируйте файл `.env.prod`, заполнив все необходимые значения, включая пароли к базе данных и SMTP-серверу.

4. Закодируйте файл `.env.prod` в формат BASE64 для добавления в GitHub Secrets:
   ```bash
   chmod +x encode_env_file.sh
   ./encode_env_file.sh
   ```

## Настройка GitHub Secrets

Добавьте следующие секреты в вашем GitHub-репозитории (Settings -> Secrets -> Actions):

1. `SSH_PRIVATE_KEY` - приватный SSH-ключ для доступа к серверу
2. `IP` - IP-адрес сервера
3. `SSH_USER` - пользователь SSH
4. `ENVIRONMENT` - окружение (`prod`)
5. `DOMAIN` - доменное имя (`perf.mtkv.ru`)
6. `ENV_FILE_BASE64` - закодированный в BASE64 файл `.env.prod`

## Запуск деплоя

После настройки GitHub Secrets, деплой можно запустить одним из следующих способов:

1. **Автоматический деплой**: при пуше в ветку `main` GitHub Actions автоматически запустит деплой.

2. **Ручной запуск**: перейдите в раздел "Actions" репозитория, выберите workflow "Deploy to Production" и нажмите "Run workflow".

## Проверка деплоя

1. После успешного деплоя приложение будет доступно по URL: `https://perf.mtkv.ru`
2. Проверьте работу приложения, авторизовавшись в системе с учетными данными администратора.
3. Убедитесь, что статические файлы и загрузки работают корректно.

## Дополнительные сведения

### Структура проекта в production

