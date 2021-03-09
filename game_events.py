from helium import hover, click, Point, set_driver
from session import create_session, load_session
from browser import open_browser, screen
from find_objects import dead_zones, find_something, default_check
from time import sleep, localtime
from datetime import datetime
import os

resources = {'wood': 0, 'stone': 0, 'chest': 0}
n = 0
dead_zone_time = 15


# return time like [hh:mm:ss]
def get_time():
    t = localtime()
    hour = '0' * (2 - len(str(t[3]))) + str(t[3])
    minute = '0' * (2 - len(str(t[4]))) + str(t[4])
    sec = '0' * (2 - len(str(t[5]))) + str(t[5])
    return '[{}:{}:{}]\t'.format(hour, minute, sec)


def mouse_click(x, y):
    hover(Point(x, y))
    sleep(0.2)
    click(Point(x, y))
    sleep(0.2)
    hover(Point(3, 3))


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
        sleep(40)

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
    global n
    n += 1

    game = screen(web)
    x, y, obj = default_check(game)
    while x > 0:
        mouse_click(x + 15, y + 14)
        dead_zones.append([x - 5, y - 5, x + 30, y + 30, datetime.now()])

        resources[obj] += 1
        game = screen(web)
        x, y, obj = default_check(game)

    if n % 10 == 0:
        print(get_time() + '\t\t\tResults:')
        print('\t\tWoods: {}\t\tStones: {}\t\tChests: {}'.format(resources['wood'], resources['stone'],
                                                                 resources['chest'], ))


def update_dead_zones():
    now = datetime.now()
    for_remove = []

    for zone in dead_zones:
        delta = now - zone[4]

        if delta.seconds > dead_zone_time:
            for_remove.append(zone)

    for zone in for_remove:
        dead_zones.remove(zone)
