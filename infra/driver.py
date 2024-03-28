from RPA.Browser.Selenium import Selenium

def driverSettings():
    browser = Selenium()
    
    # Define as opções do Chrome para execução em modo headless
    options = [
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1920,1080"
    ]

    # Inicializa o navegador com as opções especificadas
    browser.open_browser(browser="chrome", options=options)
    
    return browser
