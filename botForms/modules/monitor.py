from modules.config import (
        result_dir, 
        base_name, 
        done_file_path, 
        base_dir
        )
import os, csv, time, sys

def ListDocs():
    try:
        list_docs = []
        for doc in os.listdir(result_dir):
            if '.csv' in doc:list_docs.append(f'{result_dir}/{doc}')
    
        return list_docs
    except FileNotFoundError:
        print(f'Не обнаружена директория {result_dir}')
        sys.exit()

def ReadDoneDomain():
    def ListBase():
        list_base = []
        for base in os.listdir(base_dir):
            if '.csv' in base:list_base.append(f'{base_dir}/{base}')
        return list_base
    
    list_base = ListBase()
    all_domains = set()
    for base in list_base:
        with open(base, 'r') as file:
            for row in csv.DictReader(file):
                domain = row['Domain']
                all_domains.add(domain)


    try:
        done_domains = set()
        with open(done_file_path, 'r') as file:
            for line in file.readlines():
                domain = line.strip()
                done_domains.add(domain)
    except FileNotFoundError:
        print(f'Не обнаружен документ {done_file_path}...')
        sys.exit()
    
    percent_progress = round(len(done_domains) / (len(all_domains) / 100), 2)
    print(
            f'Всего доменов:\t\t{len(all_domains)}\n'
            f'Пройдено доменов:\t{len(done_domains)}\n'
            f'Прогресс:\t\t{percent_progress} %\n'
            )

sended_today = set()

count_domain = 0
sended_success = 0
not_connected = 0
redirect = 0

def ReadDoc(doc:str):
    global count_domain, sended_success, not_connected, sended_today, redirect
    
    current_date = time.strftime("%d/%m/%Y")

    list_domains = set()
    with open(doc, 'r') as file:
        for row in csv.DictReader(file):
            domain = row['Domain']
            try:
                date = row['Time']
                if current_date in date:sended_today.add(domain)
            except:pass
            list_domains.add(domain)
    
    type_result = doc.split('/')[1]
    if '_' in type_result:type_result = type_result.replace('_', ' ')
    if '.csv' in type_result:type_result = type_result.replace('.csv', '')
    if base_name in type_result:type_result = type_result.replace(f'{base_name} ', '')
    if 'connected' in type_result:
        not_connected = len(list_domains)
    if 'redirect' in type_result:
        redirect+=len(list_domains)
    if len(type_result) <= 1:
        type_result = "success send"
        sended_success+=len(list_domains)
    type_result = type_result.strip()
    if 'not defined' in type_result:type_result = 'Не найдено форм'
    elif 'unknown' in type_result:type_result = 'Форма с неизвестным полем'
    elif 'redirect' in type_result:type_result = 'Редирект домена'
    elif 'not connected' in type_result:type_result = 'Долгая загрузка страниц'
    else:type_result = 'Успешная отправка'
    print(f'{type_result} - {len(list_domains)}')
    count_domain+=len(list_domains)

if __name__ == '__main__':
    list_doc = ListDocs()
    ReadDoneDomain()
    for doc in list_doc:
        ReadDoc(doc=doc)
    current_sending = count_domain-not_connected
    exception_not_connectad = count_domain - not_connected - redirect
    percent_success = sended_success / (exception_not_connectad / 100) 
    print(
            f'\nУспешная обработка:\t{current_sending}\n'
            f'Процент отправленных:\t{round(percent_success, 2)} %\n'
            f'Проверено сегодня:\t{len(sended_today)}'
            )
