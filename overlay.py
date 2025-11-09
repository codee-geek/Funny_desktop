# overlay.py
import time
from Foundation import NSObject, NSTimer, NSRect
from AppKit import (
    NSWindow, NSWindowStyleMaskBorderless, NSBackingStoreBuffered,
    NSColor, NSTextField, NSFont, NSApplication, NSScreen,
    NSStatusWindowLevel, NSWindowCollectionBehaviorCanJoinAllSpaces
)

last_roast = "starting..."
window = None
label = None

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        global window, label

        screen = NSScreen.mainScreen().frame()
        w, h = 500, 44
        x = screen.size.width - w - 30
        y = 60  # bottom right

        rect = NSRect((x, y), (w, h))

        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect,
            NSWindowStyleMaskBorderless,
            NSBackingStoreBuffered,
            False
        )

        window.setOpaque_(False)
        window.setBackgroundColor_(NSColor.colorWithCalibratedWhite_alpha_(0.1, 0.85))

        # ✅ ALWAYS ON TOP ACROSS ALL SPACES / FULL SCREEN
        window.setLevel_(NSStatusWindowLevel)
        window.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces)
        window.setIgnoresMouseEvents_(True)

        window.makeKeyAndOrderFront_(None)

        label = NSTextField.alloc().initWithFrame_(NSRect((10, 10), (w - 20, h - 20)))
        label.setStringValue_(last_roast)
        label.setFont_(NSFont.systemFontOfSize_(18))
        label.setTextColor_(NSColor.whiteColor())
        label.setBezeled_(False)
        label.setDrawsBackground_(False)
        label.setEditable_(False)
        label.setFont_(NSFont.systemFontOfSize_(13))   # smaller


        window.contentView().addSubview_(label)

        # auto update label
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.35, self, "updateText:", None, True
        )

    def updateText_(self, timer):
        label.setStringValue_(last_roast)


def run_overlay():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()
