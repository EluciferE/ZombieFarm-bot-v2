from game_events import *

web = start()

for _ in range(10):
    pick_up_resources(web)

web.close()
print("Quited from browser")
