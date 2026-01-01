#!/usr/bin/python3
"""
Скрипт для настройки DKIM + Postfix
"""
import os, shutil, subprocess, json

owner_email = 'oshifda@mailnesia.com'

template_dir = 'template'
template_file = 'opendkim.conf'

template = f'{template_dir}/{template_file}'

config_dkim = f'/etc/{template_file}'
opendkim_dir = '/etc/opendkim'


############################################
# Ниже в основном про opendkim
############################################
def create_backup_etc_opendkim():
    """
    Создаем бэкап старого конфига, если он есть
    """
    status_create_config = False
    for config in os.listdir('/etc/'):
        if config == 'opendkim.conf':
            old_config = f'/etc/backup.{config}'
            config = f'/etc/{config}'
            shutil.move(config, old_config)
            status_old_config = True
    if status_create_config == True:print('Сделан бэкап старого конфига...')
    if status_create_config == False:print('Файла бэкапа нет!')
    
    try:
        shutil.copy(template, config_dkim)
        print(f'Конфиг {template} скопирован в {config_dkim}')
    except Exception as err:
        print(f'При копировании произошла ошибка:\n{err}')
            

def check_dir_opendkim():
    """
    Проверяем наличие директории opendkim 
    Если ее нет - создаем
    """
    status_opendkim_dir = False
    if os.path.exists(opendkim_dir):
        status_opendkim_dir = True
        print(f'Директория {opendkim_dir} уже существует')
    else:
        os.makedirs(opendkim_dir)
        print(f'Директория {opendkim_dir} создана')

def dkim_check_file():
    """
    Создаем или перезапиываем файлы
    в /etc/opendkim/

    """
    list_file = []
    files_dkim = ['TrustedHosts', 'KeyTable', 'SigningTable']
    for file in files_dkim:
        file = f'{opendkim_dir}/{file}'
        if not os.path.exists(file):
            with open(file, 'a') as config:
                list_file.append(file)
                print(f'Создан: {file}')
    
    return list_file

def processing_file_dkim(list_file:[]):
    """По сути просто настройка файлов"""
    for dkim_file in list_file:
        if 'Trusted' in dkim_file:
            with open(dkim_file, 'a') as file:
                file.write('127.0.0.1\nlocalhost\n')

    """Запустим как сервис"""
    run_command(command="sudo systemctl enable opendkim")
    run_command(command="sudo systemctl restart opendkim")

############################################
# Тут пока что закончили с opendkim
# Переходим к настройке Postfix
############################################

postfix_main_etc = '/etc/postfix/main.cf'
postfix_template = f'{template_dir}/main.cf'

def postfix_setting(domain:str):
    shutil.copy(postfix_template, postfix_main_etc)
    permit_net = (
            "smtpd_relay_restrictions = permit_mynetworks "
            "permit_sasl_authenticated reject_unauth_destination"
            )

    my_network_setting = (
            "mynetworks = 127.0.0.0/8 [::1]/128"
            )

    add_mydestination = (
            f"mydestination = $myhostname, mail.{domain}, localhost"
            )
    add_myhostname = f"myhostname = {domain}"
    with open(postfix_main_etc, 'a+') as file:
        file.write(
                f'{permit_net}\n'
                f'{my_network_setting}\n'
                f'{add_mydestination}\n'
                f'{add_myhostname}'
                )

def create_key(domain:str):
    path_key = f'{opendkim_dir}/{domain}'
    if not os.path.exists(path_key):
        os.makedirs(path_key)            
        print(f'Создана директория {path_key}')

    command = (
            f"sudo opendkim-genkey -D {path_key}/"
            f" --domain {domain}"
            f" --selector relay"
            )
    run_command(command=command)
    
    run_command(command=f"sudo chown :opendkim {path_key}/")
    print("Задали группу владельца")
    
    run_command(command=f"sudo chmod g+rw {path_key}/")
    print("Задали права")
    
    with open(f'{opendkim_dir}/TrustedHosts', 'a+') as file:
        file.write(f'*.{domain}\n')
        print(f"Записали домен в {opendkim_dir}/TrustedHosts")


def create_key_table(domain:str):
    """Пишем данные в KeyTable"""
    command=(
            f'echo "relay._domainkey.{domain}'
            f' {domain}:relay:{opendkim_dir}/{domain}/relay.private"'
            f' >> {opendkim_dir}/KeyTable'
            )
    run_command(command=command)

def create_note_signing(domain:str):
    """Пишем данные в SigningTable"""
    command = (
            f'echo "*@{domain}'
            f' relay._domainkey.{domain}"'
            f' >> {opendkim_dir}/SigningTable'
            )
    run_command(command=command)


def show_record(domain:str):
    path_recording = f'{opendkim_dir}/{domain}/relay.txt'
    with open(path_recording, 'r') as file:
        record = file.read()
    
    name = record.split('\t')[0].strip()
    record = record.split('(')[1]
    record = record.split(')')[0]
    record = record.replace('"', '')
    if '\n' in record:record = record.replace('\n', '')
    if '\t' in record:record = record.replace('\t', '')
    if ' ' in record:record = record.replace(' ', '')

    name = f'{name}.{domain}'
    type_record = 'TXT'
    value = f'{record}'
    divide = "*"*40
    print(
            f"\n\n{divide}\n\n"
            f"Добавь это в DNS\n\n"
            f"Name: {name}\n"
            f"Type: {type_record}\n"
            f"Value: {value}"
            f"\n\n{divide}\n\n"
            )

def redirectMail(domain:str):
    alias_domain = f"virtual_alias_domains = {domain}"
    alias_map = "virtual_alias_maps = hash:/etc/postfix/virtual"

    with open(postfix_main_etc, 'a+') as file:
        file.write(
                f"\n{alias_domain}\n"
                f"{alias_map}\n"
                )
    postfix_virtual = '/etc/postfix/virtual'
    with open(postfix_virtual, 'a+') as file:
        file.write(f"@{domain}\t{owner_email}\n")

    run_command(command="sudo postmap /etc/postfix/virtual")
    run_command(command="sudo systemctl restart postfix")

config = 'config.json'

def extractDomain():
    with open(config, 'r') as file:
        data = json.load(file)
    domain = data['domain']
    return domain


def run_command(command:str):
    """Выполняем команды"""
    try:
        print(f'RUN: {command}')
        subprocess.run(command, shell=True)
    except Exception as err:
        print(f'Error: {err}')


############################################
# Основная функция, которая собирает 
# все одно целое
############################################
def install_mailer():

    domain = extractDomain() 
    
    create_backup_etc_opendkim()
    
    check_dir_opendkim()


    list_dkim_file = dkim_check_file()
    processing_file_dkim(list_file=list_dkim_file)
    
    """Тут пошла настройка postfix"""
    
    postfix_setting(domain=domain)
    
    
    """Добавим редирект писем"""
    redirectMail(domain=domain)
    create_key(domain=domain)
    create_key_table(domain=domain)
    create_note_signing(domain=domain)
    
    chown_dkim  = f"sudo chown opendkim:opendkim /etc/opendkim/{domain}/relay.private"
    run_command(command=chown_dkim)

    run_command(command="sudo systemctl restart opendkim")

    show_record(domain=domain)

def InstallationMailer():
    try:
        install_mailer()
    except PermissionError:
        user = os.getlogin()
        print(
                f'\nСледует запускать от:\tsudo/root\n'
                f'Текущий пользователь:\t{user}'
                )


