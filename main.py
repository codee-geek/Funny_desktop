import threading
import time
import overlay
import chatbox
from detect_screen import get_active_app_info, get_browser_url
from context_map import classify
from roaster import roast
import db

# Polling interval in seconds
POLL_INTERVAL = 2.0  # Reduced frequency for better performance

def loop_logic():
    """Main loop that monitors app changes and generates roasts."""
    last_key = None
    last_context = None
    
    while True:
        try:
            info = get_active_app_info()
            app = info.get("app")
            title = info.get("window_title")
            
            if not app:
                time.sleep(POLL_INTERVAL)
                continue
            
            url = get_browser_url(app)
            context = classify(app, title, url)
            key = (app, title, url)

            # Only generate new roast if context actually changed
            if key != last_key or context != last_context:
                try:
                    line = roast(context)
                    if line:
                        print(f"ROAST [{app}]: {line}")
                        stored_line = f"{line} · {context}" if context else line
                        db.insert_message("roaster", stored_line)
                        chatbox.handle_roast_display(line)
                        last_key = key
                        last_context = context
                except Exception as e:
                    print(f"Error generating roast: {e}")

        except Exception as e:
            print(f"Error in loop_logic: {e}")
        
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    db.init_db()  # Ensure DB is initialized
    threading.Thread(target=loop_logic, daemon=True).start()
    overlay.run_overlay()  # must run on main thread
  