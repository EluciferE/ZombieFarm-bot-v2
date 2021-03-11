from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def open_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--mute-audio")
    web = webdriver.Firefox(executable_path="C:\\FirefoxWebDriver\\geckodriver.exe", options=options)
    web.maximize_window()
    return web

