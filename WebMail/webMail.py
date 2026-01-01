from SinCity.Browser.driver_chrome import driver_chrome
from SinCity.colors import RED, RESET, GREEN, YELLOW

from modules.config import base_dir
from modules.helper import helper
from modules.miniTools import (
        initMailer, 
        RecordingSendEmail, 
        CheckSendEmail,
        checkCountTemplates,
        selectTemplateLetter
        )
from modules.send_message import SendMessage
from modules.create_message import CreateSubject, CreateMessage
from modules.login import LoginWebMail, getLoginData
from modules.config import timeout_send_message

import os, sys, csv, time

def ListBase():
    list_base = []
    for base in os.listdir(base_dir):
        if '.csv' in base:list_base.append(f'{base_dir}/{base}')
    return list_base


def WebMail(login_config:str=None):
    driver = None

    initMailer()
    
    list_base = ListBase()
    if len(list_base) == 0:sys.exit(f'{RED}Нет базы для рассылки!{RESET}')
    
    """Получаем список(множество) завершенных получателей"""
    complite_list_email = CheckSendEmail()

    max_count_template = checkCountTemplates()

    user_data = getLoginData(login_config=login_config)
    limit = user_data['limit']
    sender = user_data['sender_name']
    
    """Считаем отправленные сообщения за сессию"""
    current_send_mail = 0
    
    try:
        """Логинимся в почтовик"""
        driver = LoginWebMail(login_config=login_config)

        def lenListEmails(base:str):
            count_email = set()
            with open(base, 'r') as file:
                for row in csv.DictReader(file):
                    email = row['Email']
                    count_email.add(email)
            return len(count_email)
        
        """Перебираем все базы"""
        for base in list_base:
            """Посчитаем длину списка базы для рассылки"""
            len_list_emails = lenListEmails(base=base)
            
            with open(base, 'r') as file:
                number_email = 0
                count_template = 0
                for row in csv.DictReader(file):
                    number_email+=1
                    company = row['Company']
                    email = row['Email']
                    try:name = row['Name']
                    except:name = None

                    """Если только не отправляли ранее этому получателю"""
                    if email not in complite_list_email:
                        current_send_mail+=1
                        count_template+=1
                        print(
                                f'[{GREEN}{number_email}/{RED}{len_list_emails}{RESET}] '
                                f'{company} | {email}'
                                )

                        """Получаем письмо из темплейтов"""
                        template_letter = selectTemplateLetter(
                                number_email=count_template-1
                                )
                        template_subject = template_letter[0]
                        template_message = template_letter[1]

                        subject = CreateSubject(
                                subject=template_subject,
                                company=company,
                                name=name,
                                sender_name=sender
                                )

                        message = CreateMessage(
                                message=template_message,
                                company=company,
                                name=name,
                                sender_name=sender
                                )
                        if '\u001bE' in message:
                            message = message.replace('\u001bE', '\n')
                        """Отправляем письмо"""
                        SendMessage(
                            driver, 
                            recipient=email,
                            subject=subject,
                            message=message
                            )
            
                        """Пишем в док, что отправили"""
                        RecordingSendEmail(
                                email=email, 
                                company=company, 
                                name=name, 
                                base_name=base,
                                sender=sender
                                )
                        if count_template == max_count_template:count_template = 0
                        if limit == current_send_mail:
                            if driver != None:
                                driver.quit()
                            return 

                        print(f'{YELLOW}sleep {timeout_send_message} s...{RESET}')
                        time.sleep(timeout_send_message)

        if current_send_mail == 0:
            sys.exit(f'{GREEN}Все письма отправлены!{RESET}')
    
    except KeyboardInterrupt:
        sys.exit(f'{RED}\nExit...{RESET}')
    except Exception as err:
        sys.exit(f'{RED}Error: {err}{RESET}')

    finally:
        try:
            if driver != None:
                driver.quit()
        except UnboundLocalError:
            pass

if __name__ == '__main__':
    params = sys.argv
    if len(params) == 1:
        WebMail()
    elif len(params) == 3 and '--config' in params[1] and '.json' in params[2]:
        login_config = params[2]
        if os.path.exists(login_config):
            WebMail(login_config=login_config)
        else:
            print(f'{RED}Файл конфигурации {login_config} не обнаружен{RESET}')
            helper()
    elif '--help' in params:
        helper()
    else:
        helper()
