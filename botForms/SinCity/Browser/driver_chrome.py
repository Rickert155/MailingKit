from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from SinCity.Agent.header import header

def driver_chrome():
    #profileChrome = 'ProfileChrome'

    head = header()['User-Agent']

    chrome_options = Options()
    # Подключение своего профиля
    chrome_options.add_argument(f"--user-agent={head}")
    chrome_options.add_argument("--dns-server=8.8.8.8,8.8.4.4")

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    prefs = {
        "profile.managed_default_content_settings.images": 2,
        #"profile.managed_default_content_settings.stylesheets": 2,
        #"profile.managed_default_content_settings.fonts": 2,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    

    #chrome_options.add_argument(f'--user-data-dir={profileChrome}')

    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("start-maximized")
    
    driver_chrome = webdriver.Chrome(options=chrome_options)

    return driver_chrome
