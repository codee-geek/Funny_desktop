from Foundation import NSObject, NSTimer, NSRect
from AppKit import (
    NSWindow, NSWindowStyleMaskBorderless, NSBackingStoreBuffered,
    NSColor, NSTextField, NSFont, NSApplication, NSScreen,
    NSStatusWindowLevel, NSWindowCollectionBehaviorCanJoinAllSpaces, NSView
)
from chatbox import toggle_overlay_expansion

last_roast = "starting..."
window = None
label = None
chat_active = False


def refresh_chat_view():
    """Request chat panel (if visible) to refresh its content."""
    try:
        import chatbox

        chatbox.refresh_conversation_if_visible()
    except Exception as e:
        print(f"[OVERLAY] Unable to refresh chat view: {e}")

class OverlayWindow(NSWindow):
    """A key + main borderless window that still accepts keyboard focus"""
    def canBecomeKeyWindow(self):
        return True

    def canBecomeMainWindow(self):
        return True

class ClickableView(NSView):
    """Clickable overlay background"""

    def acceptsFirstResponder(self):
        return True

    def becomeFirstResponder(self):
        return True

    def mouseDown_(self, event):
        global window
        w = self.window()
        if w:
            content = w.contentView()
            click_point = self.convertPoint_fromView_(event.locationInWindow(), None)

            # If chat container is visible, clicking inside should not toggle
            if hasattr(content, "chat_container"):
                chat_frame = content.chat_container.frame()
                if (chat_frame.origin.x <= click_point.x <= chat_frame.origin.x + chat_frame.size.width and
                        chat_frame.origin.y <= click_point.y <= chat_frame.origin.y + chat_frame.size.height):
                    w.makeKeyAndOrderFront_(None)
                    if hasattr(content, "input_box"):
                        w.makeFirstResponder_(content.input_box)
                    return

            w.makeKeyAndOrderFront_(None)
        toggle_overlay_expansion(window, label)


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        global window, label

        screen = NSScreen.mainScreen().frame()
        w, h = 500, 50
        x = screen.size.width - w - 30
        y = 60

        rect = NSRect((x, y), (w, h))
        window = OverlayWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        rect, NSWindowStyleMaskBorderless, NSBackingStoreBuffered, False
    )


        window.setOpaque_(False)
        window.setBackgroundColor_(NSColor.clearColor())
        window.setLevel_(NSStatusWindowLevel)
        window.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces)
        window.setHasShadow_(True)
        window.setIgnoresMouseEvents_(False)
        window.makeKeyAndOrderFront_(None)

        # ---- Clickable Background ----
        content = ClickableView.alloc().initWithFrame_(rect)
        window.setContentView_(content)
        content.roast_label = None
        content.setWantsLayer_(True)
        layer = content.layer()
        layer.setCornerRadius_(12)
        layer.setMasksToBounds_(True)
        layer.setBackgroundColor_(NSColor.colorWithCalibratedWhite_alpha_(0.05, 0.85).CGColor())

        # ---- Label ----
        label = NSTextField.alloc().initWithFrame_(NSRect((10, 10), (w - 20, h - 20)))
        label.setStringValue_(last_roast)
        label.setFont_(NSFont.systemFontOfSize_(14))
        label.setTextColor_(NSColor.whiteColor())
        label.setBezeled_(False)
        label.setDrawsBackground_(False)
        label.setEditable_(False)
        label.setSelectable_(False)
        content.addSubview_(label)
        content.roast_label = label

        # ---- Update timer (reduced frequency for better performance) ----
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.5, self, "updateText:", None, True
        )

        # Activate app *after* showing the window
        NSApplication.sharedApplication().activateIgnoringOtherApps_(True)

    def updateText_(self, timer):
        """Update label text if it has changed."""
        global label, last_roast
        if label and label.stringValue() != last_roast:
            label.setStringValue_(last_roast)


def run_overlay():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()
