import time
from detect_screen import get_active_app_info
from context_map import classify
from roaster import roast

def main():
    last = None
    while True:
        info = get_active_app_info()
        app, title = info["app"], info["window_title"]
        key = (app, title)


        if key != last:
            context = classify(app, title)
            print("CONTEXT:", context)   # <- ADD THIS
            line = roast(context)
            print("ROAST:", line)
            last = key

        time.sleep(1)

if __name__ == "__main__":
    main()
