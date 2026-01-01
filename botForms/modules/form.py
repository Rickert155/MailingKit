from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
        UnexpectedAlertPresentException,
        NoSuchElementException,
        ElementNotInteractableException,
        WebDriverException,
        InvalidSessionIdException
        )

from SinCity.Browser.driver_chrome import driver_chrome
from SinCity.Browser.scrolling import Scrolling
from SinCity.colors import RED, RESET, BLUE, GREEN, YELLOW
from modules.miniTools import (
        divide_line,
        RecordingNotSended,
        RecordingSuccessSend
        )

from modules.content import GenerateContent
from modules.config import contact_pages, cookie_bunner_texts

from urllib3.exceptions import ReadTimeoutError, MaxRetryError
import sys, time

"""Ищем страницы контактов(или где может быть контактная форма)"""
def OtherPages(driver:str, domain:str):
    list_link = set()
    for link in driver.find_elements(By.TAG_NAME, 'a'):
        link = link.get_attribute('href')
        if link:
            if domain in link and '#' not in link and 'mailto' not in link:
                for page in contact_pages:
                    if page in link:
                        if link[-1] == '/':link = link[:-1]
                        list_link.add(link)

    return list_link
        
"""Вводная функция обработки домена"""
def ProcessingDomain(domain:str, company:str):
    driver = None
    try:
        driver = driver_chrome()
        url = domain
        if '://' not in url:url = f'https://{domain}'
        """Максимальное время ожидание загрузки страницы"""
        driver.set_page_load_timeout(40)
        driver.get(url)
        time.sleep(2)
        current_url = driver.current_url

        Scrolling(driver=driver)
        
        CloseCookieBanner(driver)

        if domain not in current_url:
            if '://' in current_url:
                current_domain = current_url.split('://')[1]
                print(f'{RED}Редирект {domain} -> {current_domain}{RESET}')
                RecordingNotSended(domain=domain, company=company, reason="redirect")
                if driver != None:
                    driver.quit()
                return False
            else:
                RecordingNotSended(domain=domain, company=company, reason="redirect")
                if driver != None:
                    driver.quit()
                return False


        forms = SearchForms(driver=driver)

        if forms != False:
            send_form_home_page = submitForm(driver=driver, company=company)
            if send_form_home_page == True:
                RecordingSuccessSend(domain=domain, company=company)
                return True
            try:
                if 'unknown_field' in send_form_home_page:
                    RecordingNotSended(domain=domain, company=company, reason="unknown field")
            except TypeError:
                print(f'{RED}type error: bool{RESET}')
                return
            if send_form_home_page == False:
                RecordingNotSended(domain=domain, company=company, reason="not defined")
            
        if forms == False:
            list_pages = OtherPages(driver=driver, domain=domain)
            if len(list_pages) > 0:
                count_sended = 0
                count_not_defined = 0

                number_page=0

                check_forms = False
                for page in list_pages:
                    number_page+=1
                    print(f'{BLUE}[{number_page}] {page}{RESET}')
                    driver.get(page)
                    time.sleep(3)
                    Scrolling(driver=driver)
                    forms = SearchForms(driver=driver)
                    if forms != False:
                        check_forms = True
                        send_form = submitForm(driver=driver, company=company)
                        if send_form == True:
                            RecordingSuccessSend(domain=domain, company=company)
                            count_sended+=1
                            return True
                        if send_form == 'unknown_field':
                            count_not_defined+=1

                if count_not_defined > 0 and count_sended == 0:
                    RecordingNotSended(
                            domain=domain, 
                            company=company, 
                            reason="unknown field")
                
                if count_sended == 0 and count_not_defined == 0:
                    RecordingNotSended(
                            domain=domain, 
                            company=company, 
                            reason="not defined"
                            )

                if check_forms == False:
                    print(f'{RED}На страницах контактов не обнаружены формы!{RESET}')
                    RecordingNotSended(domain=domain, company=company, reason="not defined")
                    return
            if len(list_pages) == 0:
                print(f'{RED}Страницы контактов не обнаружены{RESET}')
                RecordingNotSended(domain=domain, company=company, reason="not defined")
                return


    except KeyboardInterrupt:
        print(f'{RED}\nExit...{RESET}')
        sys.exit()

    except ReadTimeoutError:
        print(f'{RED}Долгая загрузка{RESET}')
        RecordingNotSended(domain=domain, company=company, reason="not connected")
        if driver != None:
            driver.close()
            driver.quit()

    except MaxRetryError:
        print(f'Максимальное количество попыток отпкрыть сайт')
        RecordingNotSended(domain=domain, company=company, reason="not connected")
        if driver != None:
            driver.close()
            driver.quit()
    
    except WebDriverException:
        print(f'{RED}Сайт не работает{RESET}')
        RecordingNotSended(domain=domain, company=company, reason="not connected")
        if driver != None:
            driver.quit()

    except InvalidSessionIdException:
        return

    except MaxRetryError:
        return

    finally:
        if driver != None:
            driver.quit()
        print(divide_line())

def CloseCookieBanner(driver):
    cookie_buttons = driver.find_elements(By.CSS_SELECTOR, 'button, a')
    if len(cookie_buttons) > 0:
        for button in cookie_buttons:
            text = button.text
            text = text.strip().lower()
            for text_button in cookie_bunner_texts:
                if text_button in text or text == 'ok' or text == 'got it':
                    try:
                        button.click()
                        print(f'{GREEN}Закрыл баннер cookie{RESET}')
                        return
                    except:
                        continue 
            


"""Поиск формы на странице"""
def SearchForms(driver:str):
    count_form = 0
    for form in driver.find_elements(By.TAG_NAME, 'form'):
        count_input = 0
        for field_input in form.find_elements(By.TAG_NAME, 'input'):
            if field_input.is_displayed():
                count_input+=1

        if count_input >= 2:
            count_textarea=0
            for textarea in form.find_elements(By.TAG_NAME, 'textarea'):
                count_textarea+=1
            if count_textarea > 0:
                count_form+=1
    
        #if count_form > 0:
        #    print(f'Форма {count_form}')
    
    
    if count_form == 0:
        return False

    return count_form

"""Отправка формы"""
def submitForm(driver:str, company:str):
    number_form = 0
    for form in driver.find_elements(By.TAG_NAME, 'form'):
        number_form+=1
        count_input = 0
        count_textarea = 0
        for field_input in form.find_elements(By.TAG_NAME, 'input'):
            if field_input.is_displayed():
                count_input+=1
            if count_input >= 2:
                for textarea in form.find_elements(By.TAG_NAME, 'textarea'):
                    count_textarea+=1
        
        if count_textarea > 0:
            """Тут мы добавляем текст письма"""
            enter_message = EnterTextarea(element=form, company=company)
            if enter_message != False:
            
                try:
                    """Выбор первой опции из первого селекта"""
                    select_item = SelectItem(form=form)
                    
                    for field_input in form.find_elements(By.TAG_NAME, 'input'):
                        """Обрабатываем каждое поле отдельно"""
                        EnterText(element=field_input, company=company, driver=driver)
                    

                    count_click_submit_button = SubmitButton(driver=driver, form=form)

                    if count_click_submit_button > 0:
                        return True
                    if count_click_submit_button == 0:
                        return 'unknown_field'
            
                except Exception as err:
                    print(f'{RED}Error: {err}{RESET}')
                    return 'unknown_field'
    
    return False

def SelectItem(form:str):
    list_selects = form.find_elements(By.TAG_NAME, 'select')
    if len(list_selects) > 0:
        for select in list_selects:
            if select.is_displayed:
                try:
                    target_select = Select(select)
                    target_select.select_by_index(0)
                    return
                except:
                    return

"""Поиск и ввод текста в textarea"""
def EnterTextarea(element:str, company:str):
    try:
        textarea = element.find_element(By.TAG_NAME, 'textarea')
        name_textarea = textarea.get_attribute('name')
        if 'g-recaptcha-response' in name_textarea:
            return False
            
        content = GenerateContent(full_attrs="textarea", company=company)
        textarea.send_keys(content)
        time.sleep(2)
    except ElementNotInteractableException:
        pass

"""Функционал ввода текста"""
def EnterText(element:str, company:str, driver:str):
    if element.is_displayed():

        name = element.get_attribute('name')
        placeholder = element.get_attribute('placeholder')
        type_field = element.get_attribute('type')

        full_attrs = f"{name} {placeholder} {type_field}"
                    
        if type_field == 'email':
            full_attrs = 'email'
        if 'checkbox' in type_field:
            try:
                element.find_element(By.CSS_SELECTOR, '[type="checkbox"]').click()
                print('Отметил чекбокс')
                time.sleep(0.5)
                return
            except Exception as err:
                try:
                    driver.execute_script(
                            "arguments[0].checked = true;"
                            "arguments[0].dispatchEvent(new Event('change', "
                            "{ bubbles: true }));", 
                            element
                            )
                    print('Отметил чекбокс')
                    time.sleep(0.5)
                    return
                except:
                    print(f'error: {err}')
                    return

        if 'radio' in type_field:
            try:
                element.find_element(By.CSS_SELECTOR, '[type="radio"]').click()
            except:
                try:
                    driver.execute_script(
                            "arguments[0].checked = true;"
                            "arguments[0].dispatchEvent(new Event('change', "
                            "{ bubbles: true }));", 
                            element
                            )
                    time.sleep(0.5)
                    print('Отметил радио кнопку')
                    return
                except Exception as err:
                    print(f'error: {err}')
                    return
                        
        if type_field == 'submit':
            return 
        if type_field == 'file':
            return
        if type_field == 'tel':
            full_attrs = 'tel'

        content = GenerateContent(full_attrs=full_attrs, company=company)
        print(
            f'Placeholder: {placeholder}\n'
            f'Type: {type_field}\n'
            f'Name: {name}\n'
            )
        """
        Пытаемся ткнуть в поле ввода. Получается не всегда.
        Но на некоторых корявых формах помогает вводить данные
        """
        try:
            element.click()
        except:
            pass
        element.send_keys(content)
        time.sleep(2)

"""Функционал обнаружения чек-бокса капчи и клик по ней"""
def ClickAntiBotRecaptcha(driver:str, form:str):
    recaptcha = False
    try:
        recaptcha = form.find_element(By.CSS_SELECTOR, '[title="reCAPTCHA"]') 
        driver.switch_to.frame(recaptcha)
        checkbox = driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border')
        checkbox.click()
        driver.switch_to.default_content()
        recaptcha = True
    except NoSuchElementException:
        pass
    except Exception as err:
        print(f'{RED}{err}{RESET}')
    finally:
        return recaptcha

"""Отправка формы"""
def SubmitButton(driver:str, form:str):
    count_click = 0
    recaptcha = ClickAntiBotRecaptcha(driver=driver, form=form)
    if recaptcha == True:print(f'{YELLOW}Обнаружена капча, отмечен чек-бокс{RESET}')
    if recaptcha != True:print(f'{YELLOW}Капча не обнаружена{RESET}')
    
    try:
        submitInput = form.find_elements(By.CSS_SELECTOR, 'button, *[type="submit"]')
        for submit in submitInput:
            if submit.get_attribute('type') == 'submit' or submit.tag_name == 'button':
                try:
                    try:
                        action = ActionChains(driver)
                        action.move_to_element(submit).send_keys(Keys.ENTER).perform()
                    except:
                        pass
                    try:
                        driver.execute_script(
                                "arguments[0].dispatchEvent(new "
                                "MouseEvent('click', {bubbles: true}))", submit)
                    except:
                          pass  
                    time.sleep(5)
                    count_click+=1
                    break
                except Exception as err:
                    print(f'{RED}При отправке формы произошла ошибка{RESET}')

    except:
        print(f'{RED}Кнопка отправки не обнаружена!{RESET}')
    
    finally:
        return count_click

if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1:
        domain = params[1]
        ProcessingDomain(domain=domain, company='Digital Octane')
    if len(params) == 1:
        print(f'Передай параметром домен')
        sys.exit()
