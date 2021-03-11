from module import Game
from time import sleep

game = Game()
game.start()

try:
    while True:
        game.pick_up_resources()
        print(game.resources)
        sleep(5)
finally:
    game.close_browser()
