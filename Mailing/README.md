# Custom Mailing
## Первоначальные действия
```sh
sudo apt update && sudo apt install git -y
```

```sh
git clone https://github.com/Rickert155/Mailing.git
```

```sh
cd Mailing && ls -l
```

## Подготовка сервера
Для загрузки необходимых пакетов и минимальной настройки можно использовать скрипт support
```sh
python3 support
```
Будет доступно несколько режимов
- Установка пакетов + настройка
- Запуск тестов
- Удаление   


## Добавление новых темплейтов писем
Для этой задачи есть скрипт updateLetter
```sh
python3 module/updateLetter
```
При помощи него можно безболезненно добавлять новые темлейты в json.  
Для updateLetter можно добавить alias в fish или bash. Я использую оболочку fish, поэтому показываю как делать для нее
```sh
echo 'alias updateLetter="python3 module/updateLetter"' >> ~/.config/fish/config.fish
```

## config.json
В нем указывается конфигурация рассыльщика.  
- domain - указывается домен для рассылки. Значение задается во время установки
- name - от чьего имени будет рассылка. По умолчанию Vlad Ch
- user_name - имя почтового ящика для рассылки
- report - указывается получатель для репортов
- limit - устанавливается лимит на отправку писем    

## Отслеживание отправленных писем - Done/report.csv
В Done/report.csv записываются имейлы/компании/время отправки


## DNS
Инструкция по DNS со стороны сервера [DNS](https://github.com/Rickert155/Mailing/blob/main/Doc/DNS.md)

