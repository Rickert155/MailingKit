# WebMail - рассыльщик писем

## Цель проекта
Инструмент решает задачу автоматической рассылки писем через WebMail(веб-интерфейс roundcube)

## Установка
Клонируем репозиторий
```sh
git clone <url>/WebMail.git
```
Ставим модули
```sh
cd WebMail && python3 -m venv venv && ./venv/bin/pip install -r package.txt
```

## Данные для запуска рассылки
### Data/login.json
Для запуска рассыльщика используются файлы конфигурации для авторизации  
По умолчанию используется конфиг Data/login.json  
Если его нет - его необходимо создать или копировать шаблон:
```sh
cp Data/template_login.json Data/login.json
```
Возможно передать альтернативный путь до файла конфигурации:
```sh
python3 webMail.py --config other.json
```

## Тестирование создания письма для рассылки
Необходимо передать два параметра:  
Первым параметром Тему письма  
Вторым параметром Тело письма  

Пример:
```sh
python3 -m modules.create_message 'это тема' 'Это тело письма'
```
Возможно передать переменные:  
```sh
[COMPANY NAME] [NAME] [SENDER NAME]
```
Пример:
```sh
python3 -m modules.create_message \
        'Hello, [NAME]' \
        'Testing message to [COMPANY NAME]. My name is [SENDER NAME]' 
```
Эту же подсказку можно получить вызвав модуль без параметров
```sh
python3 -m modules.create_message
```

## Мультипользовательский мод
Инструмент может рассылать с нескольких аккаунтов(**не одновременно**). Для этого необходимо добавить конфигурации юзеров в Users.  
Запуск модуля:
```sh
python3 -m modules.multi_user
```
**БУДЕТ РАССЫЛКА СО ВСЕХ АККОВ, КОТОРЫЕ УКАЗАНЫ В Users**
