#!/usr/bin/python3
"""
Скрипт для автоматизации настройки сервера
"""
import subprocess, time, os, json

def install_default_packages():
    command = (
            "sudo apt update && " 
            "sudo apt install " 
            "apache2 php8.1 zip mailutils opendkim opendkim-tools ipython3" 
            " -y"
            )
    return command


def install_postfix(domain:str):

    run_command(command="sudo apt purge postfix -y && sudo apt autoremove -y")

    select_type = (
        'echo "postfix postfix/main_mailer_type select Internet Site"' 
        ' | debconf-set-selections')
    input_string = (
        f'echo "postfix postfix/mailname string {domain}"' 
        ' | sudo debconf-set-selections')
    run_command(command=select_type)
    run_command(command=input_string)


    run_command("sudo apt install postfix -y")

    install_utils = "sudo apt install dovecot-imapd dovecot-pop3d  -y"

    run_command(command=install_utils)

def user_add():
    """Тут добавить юзера sin"""
    user_add = "sudo useradd -r -s /bin/false -M sin"
    run_command(command=user_add)

config = 'config.json'

def recordingDomain(domain:str):
    data = {
            "domain":domain,
            "name":"Sin",
            "user_name":"sin",
            "report":"",
            "limit": 50
            }
    with open(config, 'w') as file:
        json.dump(data, file, indent=4)

def InitMailing():
    print("START...")
    time.sleep(0.5)
    domain = input("Domain: ").strip()
    recordingDomain(domain=domain)
    
    """Создаем юзера"""
    user_add()
    
    """Ставим postfix, dovecot и минимально настраиваем"""
    install_postfix(domain=domain)

    """
    Базовое обновление пакетов + установка минимального набора утилит
    """
    run_command(command=install_default_packages())
    
    """Добавление apache2 как сервиса и запуск apache2"""
    run_command(command="sudo systemctl enable apache2")
    run_command(command="sudo systemctl start apache2")
    
    run_command(command=f"sudo hostnamectl set-hostname {domain}")


def run_command(command:str):
    
    """
    run_command - Выполняем команды
    """

    print(f"\nRUN: {command}")
    try:
        subprocess.run(command, shell=True)
    except Exception as err:
        print(f"Error: {err}\n")


