import time
from Foundation import NSObject, NSTimer
from AppKit import NSStatusBar, NSVariableStatusItemLength, NSMenu, NSMenuItem, NSApplication

last_roast = "starting..."
statusItem = None

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        global statusItem

        statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        statusItem.setTitle_(last_roast[:20])

        menu = NSMenu.alloc().init()
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "terminate:", "")
        menu.addItem_(quit_item)
        statusItem.setMenu_(menu)

        # Schedule automatic updates every second
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, "updateTray:", None, True
        )

    def updateTray_(self, timer):
        global statusItem, last_roast
        if statusItem:
            statusItem.setTitle_(last_roast[:20])

def run_tray():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()
