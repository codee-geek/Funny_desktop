# detect_screen.py
import subprocess

def get_active_app_info():
    script = r'''
    tell application "System Events"
        set frontApp to name of first process whose frontmost is true
        tell process frontApp
            try
                set winTitle to name of window 1
            on error
                set winTitle to ""
            end try
        end tell
    end tell
    return frontApp & "||" & winTitle
    '''
    


    raw = subprocess.check_output(["osascript", "-e", script]).decode().strip()
    app, title = raw.split("||")
    return {
        "app": app,
        "window_title": title
    }
    
def get_browser_url(app):
    try:
        import subprocess, json
        script = 'tell application "Google Chrome" to return URL of active tab of front window'
        return subprocess.check_output(["osascript", "-e", script]).decode().strip()
    except:
        return None
