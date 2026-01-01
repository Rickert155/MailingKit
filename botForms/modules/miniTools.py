from SinCity.colors import RED, RESET, GREEN, BLUE
from modules.config import (
        base_dir, 
        base_name,
        done_file_path, 
        done_dir,
        result_dir,
        result_complite_file
        )
import os, csv, sys, time

def InitBot():
    if not os.path.exists(done_dir):
        os.makedirs(done_dir)
    if not os.path.exists(done_file_path):
        with open(done_file_path, 'a') as file:
            file.close()

def divide_line():
    divide = '-'*50
    return divide

def CurrentTime():
    current_time = time.strftime("%d/%m/%Y %H:%M:%S")
    return current_time

def ListBase():
    list_base = []
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(
                f'{RED}Директория {base_dir} создана!\n{RESET}'
                f'{RED}Необходимо добавить в нее базы{RESET}'
                )
        sys.exit()
    
    
    for base in os.listdir(base_dir):
        if '.csv' in base:
            list_base.append(f'{base_dir}/{base}')
    
    if len(list_base) == 0:
        print(f'{RED}Необходимо добавить базы в {base_dir}!{RESET}')
    return list_base

"""Проверка общего документа с пройденными доменами"""
def CheckDoneDomains():
    list_domain = set()
    with open(done_file_path, 'r') as file:
        for line in file.readlines():
            domain = line.strip()
            if domain not in list_domain:
                list_domain.add(domain)

    return list_domain

def RecordingDoneDomain(domain:str):
    with open(done_file_path, 'a') as file:
        file.write(f'{domain}\n')

"""Проверка доменов по таблицам"""
def CheckCompliteDomains(file_name:str):
    list_domain = set()
    with open(file_name, 'r') as file:
        for row in csv.DictReader(file):
            domain = row['Domain']
            list_domain.add(domain)
    
    return list_domain

def RecordingSuccessSend(domain:str, company:str):
    if not os.path.exists(result_dir):os.makedirs(result_dir)
    if not os.path.exists(result_complite_file):
        with open(result_complite_file, 'a') as file:
            write = csv.writer(file)
            write.writerow(['Domain', 'Company', 'Time'])

    current_time = CurrentTime()
    
    sended_domain = CheckCompliteDomains(file_name=result_complite_file)
    if domain not in sended_domain:
        with open(result_complite_file, 'a+') as file:
            write = csv.writer(file)
            write.writerow([domain, company, current_time])
        print(f'{GREEN}[{current_time}] Форма отправлена - {domain}{RESET}')



def RecordingNotSended(domain:str, company:str, reason:str):
    if not os.path.exists(result_dir):os.makedirs(result_dir)
    if ' ' in reason:reason = reason.replace(' ', '_')
    file_name = f'{result_dir}/{base_name}_{reason}.csv'
    if not os.path.exists(file_name):
        with open(file_name, 'a') as file:
            write = csv.writer(file)
            write.writerow(['Domain', 'Company', 'Reason', 'Time'])
    
    current_time = CurrentTime()
    
    recorded_domain = CheckCompliteDomains(file_name=file_name) 
    if domain not in recorded_domain:
        with open(file_name, 'a+') as file:
            write = csv.writer(file)
            if '_' in reason:reason = reason.replace('_', ' ')
            write.writerow([domain, company, reason, current_time])
        print(f'{RED}[{current_time}] Форма не отправлена - {reason}{RESET}')

