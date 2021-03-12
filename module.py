from browser import open_browser
from helium import hover, click, Point, set_driver
from session import create_session, load_session
from find_objects import recognize
from time import sleep, localtime
import os
from PIL import Image

wood = Image.open("img/wood.png")
stone = Image.open("img/stone.png")
chest = Image.open("img/chest.png")
cross = Image.open("img/cross.png")
full = Image.open("img/full.png")
zoom = Image.open("img/zoom.png")


# return time like [hh:mm:ss]
def get_time() -> str:
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


class Game:

    def __init__(self):
        self.web = open_browser()
        self.screen = Image.open('.game.png')
        self.x, self.y = 0, 0
        self.objects = []
        self.resources = {'wood': 0, 'stone': 0, 'chest': 0}

    def find_something(self, name, press=False):
        self.objects = []

        if name == 'cross':
            obj = cross
        elif name == 'full':
            obj = full
        elif name == 'zoom':
            obj = zoom
        else:
            return

        ans = recognize(self.screen, obj, 0.85, 1)
        if ans:
            self.objects = [[ans[0][0], ans[0][1]]]
            if press:
                mouse_click(ans[0][0] + obj.size[0] // 2, ans[0][1] + obj.size[1] // 2)

    def screenshot(self):
        self.web.save_screenshot('.game.png')
        sleep(2)
        self.screen = Image.open('.game.png')

    def start(self):
        if 'session.pkl' not in os.listdir():
            create_session()
        load_session(self.web)

        self.web.get('https://vk.com/app612925')
        set_driver(self.web)
        print(get_time() + "Loading game...")
        sleep(40)

        # ―――――――LOADING GAME―――――――――
        self.screenshot()
        self.find_something('cross')
        while self.objects:
            mouse_click(self.objects[0][0] + 25, self.objects[0][1] + 225)
            sleep(3)
            self.screenshot()
            self.find_something('cross')

        # ―――――――FULL SCREEN MODE―――――――
        sleep(3)
        self.screenshot()
        self.find_something('full')
        mouse_click(self.objects[0][0] + 15, self.objects[0][1] + 215)
        sleep(3)

        # ―――――――MAKE SMALL ZOOM――――――――
        self.screenshot()
        self.find_something('zoom', True)
        print(get_time() + "Successfully loaded!")

    def pick_up_resources(self):
        self.screenshot()

        self.objects = []
        array = [wood, stone, chest]
        names = ['wood', 'stone', 'chest']
        for obj in range(len(array)):
            answer = recognize(self.screen, array[obj], 0.95)
            # go throw founded objects
            # add x, y, name to return
            if answer:
                for something in answer:
                    x, y = something[0], something[1]
                    self.objects.append([x, y])
                    self.resources[names[obj]] += 1
                    mouse_click(x + array[obj].size[0] // 2, y + array[obj].size[1] // 2)
        self.screenshot()

    def print_resources(self):
        print('――――――――――――――――――――――――')
        print('\t\t\t' + get_time())
        for a, b in self.resources.items():
            print("{}: {}".format(a, b), end='\t\t')
        print('\n――――――――――――――――――――――――')

    def close_browser(self):
        self.web.close()
