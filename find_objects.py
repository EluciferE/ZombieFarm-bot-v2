from PIL import Image
import numpy as np
from datetime import datetime
from skimage.feature import match_template

dead_zones = []
dead_zone_time = 15
'''
Try to recognize object on picture with start in x,y
return array of (x, y) with objects that have chance more
than chance_sure. Max len of array is "n"
'''


def recognize(img, obj, chance_sure, n=10):
    update_dead_zones()

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


def null_with_dead_zones(result):
    for zone in dead_zones:
        for x in range(zone[0], zone[2]):
            for y in range(zone[1], zone[3]):
                result[y][x] = 0


def null_with_adding_zone(x1, y1, x2, y2, result):
    for nx in range(x1, x2):
        for ny in range(y1, y2):
            result[ny][nx] = 0


def update_dead_zones():
    now = datetime.now()
    for_remove = []

    for zone in dead_zones:
        delta = now - zone[4]

        if delta.seconds > dead_zone_time:
            for_remove.append(zone)

    for zone in for_remove:
        dead_zones.remove(zone)
