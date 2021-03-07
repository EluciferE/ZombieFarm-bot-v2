from PIL import Image
import numpy as np
from skimage.feature import match_template

wood = Image.open("img/wood.png")
stone = Image.open("img/stone.png")
chest = Image.open("img/chest.png")
cross = Image.open("img/cross.png")
full = Image.open("img/full.png")
zoom = Image.open("img/zoom.png")


# try to recognize object on picture with start in x,y
def recognize(img, obj):
    img = np.asarray(img)
    obj = np.asarray(obj)

    result = match_template(img, obj)
    result = np.round(result, 3)

    answer = np.unravel_index(np.argmax(result), result.shape)

    x, y = answer[1], answer[0]
    chance = result[y][x][0]
    print(x, y, chance)

    return x, y, chance


# compare pixels with images of objects
def default_check(img):
    array = [wood, stone, chest]
    for obj in array:
        x, y, chance = recognize(img, obj)
        if chance > 0.80:
            return x, y, array.index(obj)


def find_something(img, name):
    if name == 'cross':
        obj = cross
    elif name == 'full':
        obj = full
    elif name == 'zoom':
        obj = zoom
    else:
        return -1, -1

    x, y, chance = recognize(img, obj)
    if chance > 0.75:
        return x, y
    return -1, -1


#print(recognize(Image.open('results/episode2.png'), wood))
