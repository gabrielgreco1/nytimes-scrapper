from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

def driverSettings():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["disable-logging"])
    
    # # Redirecionar stdout e stderr para devnull para suprimir logs indesejados
    # service = Service(ChromeDriverManager().install())
    # service.log_path = os.devnull
    # if sys.platform == "win32":
    #     service.creationflags = 0x08000000  # CREATE_NO_WINDOW

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver
