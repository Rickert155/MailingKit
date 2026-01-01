from SinCity.Browser.driver_chrome import driver_chrome
from SinCity.colors import RED, GREEN, BLUE, RESET

from modules.miniTools import (
        initParser,
        RecordResult,
        current_time
        )
from modules.config import contact_pages, base_dir, done_file
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import sys, csv, os

"""Проверяем, является ли домено доменом, или это URL"""
def processingDomain(domain:str):
    if '://' in domain:domain = domain.split('://')[1]
    if '/' in domain:domain = domain.split('/')[0]
    return domain

def ListPages(driver, domain:str):
    list_pages = set()

    list_link = driver.find_elements(By.TAG_NAME, 'a')
    if len(list_link) > 0:
        for link in list_link:
            link = link.get_attribute('href')
            for page in contact_pages:
                try:
                    if link != None and page in link \
                        and 'mailto:' not in link \
                        and '#' not in link \
                        and domain in link:
                        list_pages.add(link)
                except TypeError:
                    print(f'{RED}incorrect link: {link}{RESET}')
    return list_pages 

def print_emails(email_list:list[str]):
    number_email = 0
    for email in email_list:
        number_email+=1
        print(f'{GREEN}[{number_email}] {email}{RESET}')


def Generics(domain:str, company:str):
    """Зададим стартовое состояние для driver"""
    driver = None
    email_list = []
    try:
        initParser()
        
        """Лишний раз убедимся, что получили домен, а не URL"""
        domain = processingDomain(domain=domain)
        
        driver = driver_chrome()
        driver.set_page_load_timeout(40)
        url = f'http://{domain}'
        driver.get(url)
        
        """Получим список страниц контактов"""
        list_pages = ListPages(driver, domain=domain)
        if len(list_pages) == 0:print(f'{RED}The list of contact pages is empty{RESET}')

        email_list = searchEmail(driver)
        if email_list != None and len(email_list) > 0:
            #print_emails(email_list=email_list)
            return email_list
        if len(email_list) == 0:
            if len(list_pages) > 0:
                for i, page in enumerate(list_pages):
                    print(f'{BLUE}[{i+1}] {page}{RESET}')
                    driver.get(page)
                    email_list = searchEmail(driver)
                    if len(email_list) > 0:
                        return email_list
            else:
                print(f'{RED}Страниц контактов не найдено обнаружены{RESET}')

        if len(email_list) == 0:
            print(f'{RED}Имейлы не обнаружены{RESET}')

    except KeyboardInterrupt:
        sys.exit(f'{RED}\nExit...{RESET}')
    except Exception as err:
        print(f'{RED}{err}{RESET}')
    finally:
        with open(done_file, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([domain, company, current_time()])

        if driver != None:
            driver.quit()
    
    return email_list

#######################################
#           Поиск дженерика          #
#######################################
def searchEmail(driver) -> list[str]:
    page_source = driver.page_source
    bs = BeautifulSoup(page_source, 'lxml')
    
    list_email = []

    list_tag = ['a', 'span', 'p', 'div', 'strong']
    for tag in bs.find_all(list_tag):
        text = tag.get_text(separator=" ")
        text = text.split()
        for word in text:
            word = word.strip().lower()
            if '@' in word and word not in list_email:
                list_email.append(word)
    
    return list_email

def ListBase() -> list[str]:
    list_base = set()
    for base in os.listdir(base_dir):
        if '.csv' in base:
            list_base.add(f'{base_dir}/{base}')
    return list_base

def CompliteListDomain() -> list[str]:
    list_domain = set()
    if os.path.exists(done_file):
        with open(done_file, 'r') as file:
            for row in csv.DictReader(file):
                domain = row['Domain']
                list_domain.add(domain)
    
    return list_domain


if __name__ == '__main__':
    params = sys.argv
    if len(params) > 2 and '--debug' in params[1]:
        domain = params[2]
        email_list = Generics(domain=domain, company=company)
        if email_list != None and len(email_list) > 0:
            print_emails(email_list=email_list)
            RecordResult(
                    domain=domain, 
                    email=email,
                    company=company,
                    category=category,
                    location=location
                    )
    else:
        list_base = ListBase()
        if list_base:
            for base in list_base:
                with open(base, 'r') as file:
                    complite_list_domain = CompliteListDomain()
                    number_domain = 0
                    for row in csv.DictReader(file):
                        number_domain+=1
                        domain = row['Domain']
                        company = row['Company']
                        location = row.get('Location')
                        category = row.get('Category')
                        
                        if domain not in complite_list_domain:
                            print(f'{GREEN}[{number_domain}] {domain}{RESET}')
                            email_list = Generics(domain=domain, company=company)
                            if email_list != None and len(email_list) > 0:
                                print_emails(email_list=email_list)
                                for email in email_list:
                                    RecordResult(
                                            domain=domain, 
                                            email=email,
                                            company=company,
                                            category=category,
                                            location=location
                                            )
