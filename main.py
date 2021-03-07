from game_events import start, pick_up_resources


web = start()


pick_up_resources(web)

web.close()
web.quit()
print("Quited from browser")
