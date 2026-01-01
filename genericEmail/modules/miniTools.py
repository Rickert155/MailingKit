from SinCity.colors import RED, RESET
from modules.config import base_dir, result_dir, result_file, done_dir, done_file
import sys
import os
import csv
import time

def current_time() -> str:
    return time.strftime('%d/%m/%Y %H:%M:%S')

def initParser():
    if not os.path.exists(done_dir):os.makedirs(done_dir)
    if not os.path.exists(result_dir):os.makedirs(result_dir)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        sys.exit(
                f'{RED}Директория {base_dir} создана! '
                f'Необходимо добавить базу в {base_dir}{RESET}'
                )
    if not os.path.exists(done_file):
        with open(done_file, 'a') as file:
            write = csv.writer(file)
            write.writerow(['Domain', 'Company', 'Date'])

def RecordResult(domain:str, email:str, company:str, location:str, category:str):
    if not os.path.exists(result_file):
        with open(result_file, 'a') as file:
            write = csv.writer(file)
            write.writerow(['Domain', 'Email', 'Company', 'Location', 'Category'])

    with open(result_file, 'a+') as file:
        write = csv.writer(file)
        write.writerow([domain, email, company, location, category])

