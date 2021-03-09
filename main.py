from game_events import start, pick_up_resources, update_dead_zones
from time import sleep

web = start()
try:
    while True:
        pick_up_resources(web)
        update_dead_zones()
        sleep(5)
finally:
    web.close()
    web.quit()
    print("Quited from browser")
