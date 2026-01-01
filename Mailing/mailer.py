from email.message import EmailMessage
from lib.miniTools import (
        configInfo, 
        initMailer,
        count_email,
        reportRecipient,
        ListSentEmail,
        Recording
        )
from lib.config import config, base_dir
from lib.colors import RED, RESET, GREEN, BLUE
from lib.createLetter import generateLetter, get_count_letter
import csv, time, smtplib

def processingBase(base:str):
    """Получим количество имейлов в базе"""
    all_email = count_email(base=base)
    
    """Получим количество шаблонов писем"""
    count_template = get_count_letter()
    
    """Собираем список получателей, кому уже отправили письмо"""
    list_email = ListSentEmail()

    """Сколько всего уже отправили из базы"""
    len_list_email = len(list_email)

    with open(base, 'r') as file:
        number_user = 0
        
        """Счетчик для шаблонов писем"""
        count = 0

        reportRec, LIMIT = reportRecipient()
        
        for row in csv.DictReader(file):
            email = row['Email']

            try:company = row['Company']
            except:company = None
            try:name = row['Name']
            except:name = None

            if email not in list_email:
                count+=1
                number_user+=1

                print(
                        f'[{number_user}/{all_email-len_list_email}] '
                        f'{name}: {company}\n{GREEN}{email}{RESET}\n'
                        )

                theme, body = generateLetter(count=count, email=email, company=company, name=name)
                print(
                        f"Theme: {BLUE}{theme}{RESET}\n"
                        f"Body: {GREEN}{body}{RESET}\n"
                        )
            
                """Отправляем письмо"""
                Send(
                        recipient=email, 
                        theme=theme, 
                        message=body
                        )
                Recording(email=email, name=name, company=company)

                """
                Сбрасываем счетчик, если 
                он равен количеству темплейтов
                """
                if count == count_template:count = 0

                """Сравниваем с лимитом на отправку"""
                if number_user == LIMIT or number_user == all_email-len_list_email:
                    domain, name, user_name = configInfo()
                    Send(
                            recipient=reportRec,
                            theme=f"Отчет о завершении рассылки: {user_name}@{domain}",
                            message=f"Отправлено писем: {number_user}\n{user_name}@{domain}"
                            )
                    break
                
                time.sleep(120)
        if number_user == 0:
            print(f"{GREEN}Рассылка завершена. Получателей не осталось!{RESET}")

def Mailer():
    list_base = initMailer()
    domain, name, user_name = configInfo()

    number_base = 0
    if list_base != False:
        for base in list_base:
            number_base+=1
            print(f"{RED}[{number_base}]{RESET} {BLUE}{base}{RESET}")
            try:
                processingBase(base=base)
            except Exception as err:
                """В случае прерывания репортим на почту"""
                Send(
                        recipient=reportRecipient()[0],
                        theme=f"Аварийное завершении рассылки: {user_name}@{domain}",
                        message=f"Рассылка прервана!\n{err}\n{user_name}@{domain}"
                        )

    if list_base == False:print(f'List of base empty!')


#######################################
# Основная фунция рассыльщика
#######################################
def Send(recipient:str=None, theme:str=None, message:str=None):
    domain, name, user_name = configInfo()
    
    msg = EmailMessage()
    msg['From'] = f'{name} <{user_name}@{domain}>'
    msg['To'] = recipient
    msg['Subject'] = theme 
    msg.set_content(message)
    
    try:
        with smtplib.SMTP("localhost", 25) as smtp:
            smtp.send_message(msg)
            print(f"Send Message To: {recipient}")
    except Exception as err:
        print(f"ERROR Send Message To: {recipient}: {err}")
    finally:
        divide = '='*40
        print(f'\n{divide}\n')

try:
    Mailer()
except KeyboardInterrupt:print(f'{RED}\nExit...{RESET}')
