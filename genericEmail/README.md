# Search generic Emails

## Назначение
Инструмент решает задачу сбора имейлов со списка сайтов

## Установка
Склонируем в созданную директорию и поставим зависимости в окружение
```sh
mkdir ~/Parser && cd ~/Parser && git clone https://github.com/Rickert155/genericEmail && cd genericEmail
```

```sh
python3 -m venv venv && ./venv/bin/pip install -r package.txt && ./venv/bin/pip freeze
```

## Режим отладки
Можно запускать парсер в режиме отладки. Для этого необходимо указкать параметр --debug и указать домен
```sh
python3 Generics.py --debug domain.com
```

## Сбор имейлов
В директорию Base необходимо добавить базу с доменами в формате csv. Название не имеет значение. Колонки, обязательные:

----------------
|Domain|Company|
----------------

Парсер будет обходить список доменов и писать результат в директорию Result/

## Запуск сервиса
Инструмент можно повесить как демона systemd на сервер или виртульную машину. Для этого подготовлен generic@.service.  
**ВНИМАНИЕ!** - в данном юните подразумевается, что инструмент находится в директории ~/Parser/genericEmail. Если путь отличается - его необходимо поправить в юните.  
Копируем сервис
```sh
sudo cp generic@.service /etc/systemd/system/
```
Обновляем базу сервисов
```sh
sudo systemctl daemon-reload
```
Запускаем(user заменить на вашего текущего юзера)
```sh
sudo systemctl start generic@user
```
При необходимости можно добавить в автозагрузку
```sh
sudo systemctl enable generic@user
```
