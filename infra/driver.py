from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from robocorp.tasks import task

def driverSettings():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-web-security')
    options.add_argument("--start-maximized")
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument("--window-size=1280,720") 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=None, options=options)
    return driver
