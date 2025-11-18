import subprocess

def get_active_app_info():
    """Get the currently active application and window title."""
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
    try:
        raw = subprocess.check_output(
            ["osascript", "-e", script],
            stderr=subprocess.DEVNULL,
            timeout=2
        ).decode().strip()
        if "||" in raw:
            app, title = raw.split("||", 1)
            return {"app": app, "window_title": title}
        return {"app": None, "window_title": None}
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError):
        return {"app": None, "window_title": None}


def get_browser_url(app):
    """
    Return URL of active tab for Chrome or Safari.
    If no window is open, returns None instead of raising.
    """
    if app not in ("Google Chrome", "Safari"):
        return None

    if app == "Google Chrome":
        script = r'''
        tell application "Google Chrome"
            if (count of windows) > 0 then
                tell front window
                    if (count of tabs) > 0 then
                        return URL of active tab
                    else
                        return "NO_TABS"
                    end if
                end tell
            else
                return "NO_WINDOW"
            end if
        end tell
        '''
    else:
        script = r'''
        tell application "Safari"
            if (count of windows) > 0 then
                tell front window
                    return URL of current tab
                end tell
            else
                return "NO_WINDOW"
            end if
        end tell
        '''

    try:
        output = subprocess.check_output(
            ["osascript", "-e", script],
            stderr=subprocess.DEVNULL,
            timeout=2
        ).decode().strip()
        if output in ("NO_WINDOW", "NO_TABS", ""):
            return None
        return output
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
