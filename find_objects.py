from PIL import Image
import numpy as np
from datetime import datetime
from skimage.feature import match_template

wood = Image.open("img/wood.png")
stone = Image.open("img/stone.png")
chest = Image.open("img/chest.png")
cross = Image.open("img/cross.png")
full = Image.open("img/full.png")
zoom = Image.open("img/zoom.png")

dead_zones = []

'''
Try to recognize object on picture with start in x,y
return array of (x, y) with objects that have chance more
than chance_sure. Max len of array is "n"
'''


def recognize(img, obj, chance_sure, n=10):
    objects = []
    img = np.asarray(img)

    ox, oy = obj.size
    obj = np.asarray(obj)

    result = match_template(img, obj)
    result = np.round(result, 3)

    null_with_dead_zones(result)

    answer = np.unravel_index(np.argmax(result), result.shape)

    x, y = answer[1], answer[0]
    chance = result[y][x][0]
    # Check objects in loop
    while chance > chance_sure and len(objects) < n:
        objects.append([x, y])

        dead_zones.append([x - ox // 2, y - oy // 2, x + ox, y + oy, datetime.now()])
        null_with_adding_zone(x - ox // 2, y - oy // 2, x + ox, y + oy, result)

        answer = np.unravel_index(np.argmax(result), result.shape)

        x, y = answer[1], answer[0]
        chance = result[y][x][0]

    return objects


def find_something(img, name):
    if name == 'cross':
        obj = cross
    elif name == 'full':
        obj = full
    elif name == 'zoom':
        obj = zoom
    else:
        return -1, -1

    ans = recognize(img, obj, 0.8, 1)
    if ans:
        return ans[0][0], ans[0][1]
    return -1, -1


# compare pixels with images of objects
def default_check(img):
    objects = []
    array = [wood, stone, chest]
    names = ['wood', 'stone', 'chest']
    for obj in range(len(array)):
        answer = recognize(img, array[obj], 0.95)
        # go throw founded objects
        # add x, y, name to return
        if answer:
            for something in answer:
                objects.append([something[0], something[1], names[obj]])
    return objects


def null_with_dead_zones(result):
    for zone in dead_zones:
        for x in range(zone[0], zone[2]):
            for y in range(zone[1], zone[3]):
                result[y][x] = 0


def null_with_adding_zone(x1, y1, x2, y2, result):
    for nx in range(x1, x2):
        for ny in range(y1, y2):
            result[ny][nx] = 0
