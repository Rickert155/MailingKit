from selenium.webdriver.common.by import By

from SinCity.colors import RED, RESET, GREEN, BLUE
from modules.config import base_dir, timeout_click

import sys, time

def successSend():
    print(f'{GREEN}Успешная отпарвка{RESET}\n')

def SendMessage(driver, recipient:str, subject:str, message:str):
    try:
        button_compose = driver.find_element(By.CLASS_NAME, 'compose')
        button_compose.click()
        time.sleep(timeout_click)
    except Exception as err:
        sys.exit(f'{RED}compose не обнаружен{RESET}')
    
    try:
        recipient_fields = driver.find_elements(By.TAG_NAME, 'input')
        if len(recipient_fields) > 0:
            for recipient_field in recipient_fields:
                try:
                    role_combobox = recipient_field.get_attribute('role')
                    autocomplete_list = recipient_field.get_attribute(
                            'aria-autocomplete'
                            )
                    if role_combobox == 'combobox' and autocomplete_list == 'list':
                        recipient_field.send_keys(recipient)
                        print(f'{BLUE}To:{RESET}\t\t{recipient}')
                        time.sleep(timeout_click)
                        break
                except:
                    print(err)
    except:
        sys.exit(f'{RED}ошибка при опредении поля для ввода получателя{RESET}')
    
    try:
        subject_field = driver.find_element(By.ID, 'compose-subject')
        subject_field.send_keys(subject)
        print(f'{BLUE}Subject:{RESET}\t{subject}')
        time.sleep(timeout_click)
    except:
        sys.exit(f'{RED}ошибка при обнаружении поля для темы письма{RESET}')

    try:
        message_field = driver.find_element(By.NAME, '_message')
        message_field.send_keys(message)
        print(f'{BLUE}Message:{RESET}\t{message}')
        time.sleep(timeout_click+1)
    except:
        sys.exit(
                f'{RED}ошибка при обнаружении поля для ввода сообщения\n'
                f'Необходимо проверить настройки: Настройки -> Создание сообщений'
                f' -> Создавать сообщения в HTML - поставить "никогда"{RESET}')

    try:
        try:
            button = driver.find_element(By.ID, 'rcmbtn111').click()
            successSend()
            time.sleep(timeout_click)
        except:
            pass
        try:
            button = driver.find_element(By.ID, 'rcmbtn111-clone').click()
            successSend()
            time.sleep(timeout_click)
        except:
            pass
    except Exception as err:
        sys.exit(f'{RED}ошибка при поиске/нажитии кнопи отправки письма{RESET}\n{err}')
