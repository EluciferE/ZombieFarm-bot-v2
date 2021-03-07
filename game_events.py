from helium import *
from session import *
from browser import *
from find_objects import *
from time import *
import os

resources = ['wood', 'stone', 'chest']


# return time like [hh:mm:ss]
def get_time():
    t = localtime()
    hour = '0' * (2 - len(str(t[3]))) + str(t[3])
    minute = '0' * (2 - len(str(t[4]))) + str(t[4])
    sec = '0' * (2 - len(str(t[5]))) + str(t[5])
    return '[{}:{}:{}]\t'.format(hour, minute, sec)


def mouse_click(x, y):
    hover(Point(x, y))
    sleep(1)
    click(Point(x, y))


def start():
    OFFSET = 200

    if not 'session.pkl' in os.listdir():
        create_session()

    web = None

    try:
        web = open_browser()
        load_session(web)

        web.get('https://vk.com/app612925')
        set_driver(web)
        print(get_time() + "Loading game...")
        sleep(50)

        # ―――――――LOADING GAME―――――――――
        game = screen(web)
        x, y = find_something(game, 'cross')
        mouse_click(x + 25, y + OFFSET + 25)
        sleep(3)

        # ―――――――FULL SCREEN MODE―――――――

        game = screen(web)
        x, y = find_something(game, 'full')
        mouse_click(x + 15, y + OFFSET + 15)
        sleep(3)

        # ―――――――MAKE SMALL ZOOM――――――――
        game = screen(web)
        x, y = find_something(game, 'zoom')
        mouse_click(x + 15, y + 15)
        print(get_time() + "Successfully loaded!")
        return web

    except Exception as error:
        print(get_time() + "Something went wrong with browser: ", error)
        if web:
            web.close()
            web.quit()


def pick_up_resources(web):
    n = 0
    amount = [0, 0, 0]
    game = screen(web)
    x, y, obj = default_check(game)
    while x > 0:
        n += 1
        mouse_click(x + 15, y + 14)
        #game.save('results/episode' + str(n) + '.png')
        amount[obj] += 1
        print(get_time() + 'Took {}'.format(resources[obj]))
        game = screen(web)
        x, y, obj = default_check(game)
