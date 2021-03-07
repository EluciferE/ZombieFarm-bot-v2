from selenium import webdriver
from time import sleep
import pickle


def create_session():
    web = webdriver.Firefox(executable_path="C:\\FirefoxWebDriver\\geckodriver.exe")
    web.get("https://vk.com/")
    GOT_COOKIE = False
    while not GOT_COOKIE:
        sleep(1)

        cookies = web.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'remixusid':
                GOT_COOKIE = True

        pickle.dump(web.get_cookies(), open("session.pkl", "wb"))

    web.close()


def load_session(web):
    web.get('https://vk.com/')
    cookies = pickle.load(open("session.pkl", "rb"))
    for cookie in cookies:
        web.add_cookie(cookie)
