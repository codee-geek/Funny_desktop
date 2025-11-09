import time
import threading
import tray
from detect_screen import get_active_app_info, get_browser_url
from context_map import classify
from roaster import roast

def loop():
    last = None
    while True:
        info = get_active_app_info()
        app, title = info["app"], info["window_title"]
        url = get_browser_url(app)

        context = classify(app, title, url)
        key = (app, title, url)

        if key != last:
            line = roast(context)
            print("ROAST:", line)
            tray.last_roast = line
            last = key

        time.sleep(1)

if __name__ == "__main__":
    # run background logic in thread
    threading.Thread(target=loop, daemon=True).start()

    # tray runs **here** on the main thread
    tray.run_tray()
