from selenium.webdriver.common.by import By

from SinCity.Browser.driver_chrome import driver_chrome
from SinCity.colors import RED, RESET, GREEN

from modules.config import data_login
from modules.config import timeout_login

import json, os, time, sys

def getLoginData(login_config:str=None):
    if login_config == None:path_file = data_login
    if login_config != None:path_file = login_config
    if os.path.exists(path_file):
        with open(path_file, 'r') as file:
            data = json.load(file)
            
            auth_data = {
                    "sender_name":data['sender_name'],
                    "login":data['login'],
                    "password":data['password'],
                    "url_login":data['url'],
                    "limit":data['limit']
                    }
            return auth_data

    if not os.path.exists(data_login):
        sys.exit(f'{RED}Добавь {data_login}{RESET}')

def checkCaptcha(driver):
    page_source = driver.page_source
    if 'Cloudflare' in page_source:
        return True
    else:
        return False

def auth_web_mail(driver, login:str, password:str, url:str):
    try:
        driver.get(url)
        time.sleep(3)

        captcha = checkCaptcha(driver)
        if captcha == True:
            return 'Captcha'
        if captcha == False:
            
            try:
                print(f'login:\t\t{login}')
                login_field = driver.find_element(By.ID, 'rcmloginuser')
                login_field.send_keys(login)
                time.sleep(timeout_login)
            except Exception as err_login:
                sys.exit(f'{RED}Ошибка при вводе логина\n{err_login}{RESET}')

            try:
                censurship_password = '*'*len(password)
            
                print(f'password:\t{censurship_password}')
                password_field = driver.find_element(By.ID, 'rcmloginpwd')
                password_field.send_keys(password)
                time.sleep(timeout_login)
            except Exception as err_password:
                sys.exit(f'{RED}Ошибка при вводе пароля\n{err_password}{RESET}')

            try:
                button_login = driver.find_element(By.ID, 'rcmloginsubmit')
                button_login.click()
                time.sleep(timeout_login)
            except Exception as err_button:
                sys.exit(f'{RED}Ошибка при нажатии на кнопку\n{err_button}{RESET}')
        
        return 'OK'

    except KeyboardInterrupt:
        sys.exit(f'{RED}\nExit...{RESET}')

    except Exception as err:
        print(
                f'{RED}Авторизация не пройдена!{RESET}\n'
                f'Error: {err}'
                )
        if driver != None:
            driver.quit()

def LoginWebMail(login_config:str=None):
    driver = None
    try:
        auth_data = getLoginData(login_config=login_config)
    
        login = auth_data['login']
        password = auth_data['password']
        url_login = auth_data['url_login']

        print(f'url:\t\t{url_login}')
    
        login_state = False
        count_login, max_count_login = 0, 3
        while login_state != True:
            count_login+=1
            driver = driver_chrome()
            auth = auth_web_mail(driver, login=login, password=password, url=url_login)
            if auth == 'Captcha':
                print(
                        f'{RED}[{count_login}/{max_count_login}] '
                        f'Обнаружена проверка анти-бот!{RESET}'
                        )
                if driver != None:
                    driver.quit()

            if auth == 'OK':
                login_state = True
                return driver

            if count_login == max_count_login:
                if driver != None:
                    driver.quit()
                return None
    
    except Exception as err:
        sys.exit(f'{RED}{err}{RESET}')
        if driver != None:
            driver.quit()

if __name__ == '__main__':
    auth = LoginWebMail()
