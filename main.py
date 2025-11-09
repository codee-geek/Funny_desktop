import time
import threading
import overlay
from detect_screen import get_active_app_info, get_browser_url
from context_map import classify
from roaster import roast

def loop_logic():
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
            overlay.last_roast = line
            last = key

        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=loop_logic, daemon=True).start()
    overlay.run_overlay()   # <-- NOW runs on the main thread
