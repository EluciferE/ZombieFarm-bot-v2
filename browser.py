from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image
from time import sleep


def open_browser():
    options = Options()
    options.add_argument("--headless")
    web = webdriver.Firefox(executable_path="C:\\FirefoxWebDriver\\geckodriver.exe", options=options)
    web.maximize_window()
    return web


def screen(web):
    web.save_screenshot('.game.png')
    sleep(3)
    game = Image.open('.game.png')
    return game
