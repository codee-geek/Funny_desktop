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
        w, h = 500, 50
        x = screen.size.width - w - 30
        y = 60

        rect = NSRect((x, y), (w, h))

        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            rect,
            NSWindowStyleMaskBorderless,
            NSBackingStoreBuffered,
            False
        )

        # appearance
        window.setOpaque_(False)
        window.setBackgroundColor_(NSColor.clearColor())
        window.setLevel_(NSStatusWindowLevel)
        window.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces)
        window.setIgnoresMouseEvents_(True)
        window.setHasShadow_(True)
        window.makeKeyAndOrderFront_(None)

        # ---- Rounded Glass Container ----
        content = window.contentView()
        content.setWantsLayer_(True)
        layer = content.layer()
        layer.setCornerRadius_(12)
        layer.setMasksToBounds_(True)
        layer.setBackgroundColor_(NSColor.colorWithCalibratedWhite_alpha_(0.05, 0.85).CGColor())

        # Label
        label = NSTextField.alloc().initWithFrame_(NSRect((10, 10), (w - 20, h - 20)))
        label.setStringValue_(last_roast)
        label.setFont_(NSFont.systemFontOfSize_(14))
        label.setTextColor_(NSColor.whiteColor())
        label.setBezeled_(False)
        label.setDrawsBackground_(False)
        label.setEditable_(False)
        label.setSelectable_(False)
        content.addSubview_(label)

        # auto update
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
