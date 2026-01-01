from lib.config import config
from lib.config import base_dir, done_dir, report_path
import os, json, csv, time

#######################################
# Тут мы читает json с конфигом и 
# возвращаем домен/user_name/name 
# для рассылки
#######################################
def configInfo():
    try:
        with open(config, 'r') as file:
            data = json.load(file)
            domain = data['domain']
            name = data['name']
            user_name = data['user_name']
        return domain, name, user_name
    except FileNotFoundError:
        print(f'Отсутствует {config}\n')

def reportRecipient():
    try:
        with open(config, 'r') as file:
            data = json.load(file)
            rec = data['report']
            limit = data['limit']
        return rec, limit
    except FileNotFoundError:
        print(f'Отсутствует {config}\n')

#######################################
# Инициализируем рассыльщик
#######################################
def initMailer():
    if not os.path.exists(done_dir):os.makedirs(done_dir) 
    if not os.path.exists(report_path):
        with open(report_path, 'a') as file:
            write = csv.writer(file)
            write.writerow(['Email', 'Name', 'Company', 'Time'])

    list_base = []
    
    pl_add_base = f'Add base to dir {base_dir}'
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(pl_add_base)
        return False 
    
    if os.path.exists(base_dir):
        for base in os.listdir(base_dir):
            if '.csv' in base:
                base = f'{base_dir}/{base}'
                list_base.append(base)
        if len(list_base) == 0:
            print(pl_add_base)
            return False
        else:
            return list_base
    


#######################################
# Тут просто считаем количество 
# имейлов из базы
#######################################
def count_email(base:str):
    number = 0
    with open(base, 'r') as file:
        for row in csv.DictReader(file):
            number+=1
            email = row['Email']
    return number


#######################################
# Собираем список получаетелей, 
# куда уже отправили письма
#######################################
def ListSentEmail():
    list_email = []
    with open(report_path, 'r') as file:
        for row in csv.DictReader(file):
            email = row['Email']
            list_email.append(email)
    return list_email

#######################################
# Записываем получателей, 
# кому отправили
#######################################
def Recording(email:str, company:str=None, name:str=None):
    current_time = time.strftime("%d/%m/%Y %H:%M:%S")
    with open(report_path, 'a+') as file:
        write = csv.writer(file)
        write.writerow([email, name, company, current_time])
