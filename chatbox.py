from Foundation import NSRect
from AppKit import NSTextField, NSColor, NSFont

expanded = False

def toggle_overlay_expansion(window):
    """Toggle overlay expansion with animation and input box"""
    global expanded
    frame = window.frame()
    w = frame.size.width
    x = frame.origin.x
    y = frame.origin.y
    new_h = 200 if not expanded else 50
    new_rect = NSRect((x, y), (w, new_h))
    window.setFrame_display_animate_(new_rect, True, True)

    content = window.contentView()

    if not expanded:
        # ---- EXPAND: Add input box ----
        input_box = NSTextField.alloc().initWithFrame_(((10, 60), (w - 20, 30)))
        input_box.setPlaceholderString_("Type your reply here...")
        input_box.setFont_(NSFont.systemFontOfSize_(13))
        input_box.setTextColor_(NSColor.whiteColor())
        input_box.setBezeled_(True)
        input_box.setBezelStyle_(1)
        input_box.setDrawsBackground_(True)
        input_box.setBackgroundColor_(NSColor.colorWithCalibratedWhite_alpha_(0.1, 0.8))
        input_box.setEditable_(True)
        input_box.setSelectable_(True)

        content.addSubview_(input_box)
        content.input_box = input_box
    else:
        # ---- COLLAPSE: Remove input box ----
        if hasattr(content, "input_box"):
            content.input_box.removeFromSuperview()
            delattr(content, "input_box")

    expanded = not expanded
