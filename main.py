from game_events import start, pick_up_resources
from time import sleep

web = start()
try:
    while True:
        pick_up_resources(web)
        sleep(5)
finally:
    web.close()
    web.quit()
    print("Quited from browser")
