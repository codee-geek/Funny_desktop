from Foundation import NSRect
from AppKit import NSTextField, NSColor, NSFont

expanded = False


class ReplyField(NSTextField):
    # def acceptsFirstResponder(self):
    #     print("[DEBUG] acceptsFirstResponder called")
    #     return True

    # def becomeFirstResponder(self):
    #     print("[DEBUG] becomeFirstResponder called")
    #     return True

    # def resignFirstResponder(self):
    #     print("[DEBUG] resignFirstResponder called")
    #     return True

    def keyDown_(self, event):
        print("[DEBUG] keyDown_ event received:", event.keyCode())
        if event.keyCode() == 36:  # Return key
            text = self.stringValue()
            print("User replied:", text)
            self.setStringValue_("")
        else:
            super(ReplyField, self).keyDown_(event)


    def acceptsFirstResponder(self):
        return True

    def becomeFirstResponder(self):
        return True

    def keyDown_(self, event):
        if event.keyCode() == 36:  # Return key
            text = self.stringValue()
            print("User replied:", text)
            self.setStringValue_("")
        else:
            # PyObjC requires explicit super call with class name
            super(ReplyField, self).keyDown_(event)
            
    


def toggle_overlay_expansion(window):
    """Expand or collapse overlay with input box."""
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
        # ---- EXPAND ----
        input_height = 30
        margin = 10
        input_y = 10

        input_box = ReplyField.alloc().initWithFrame_(((margin, input_y), (w - 2 * margin, input_height)))
        input_box.setPlaceholderString_("Type your reply here...")
        input_box.setFont_(NSFont.systemFontOfSize_(13))
        input_box.setTextColor_(NSColor.whiteColor())
        input_box.setBezeled_(False)
        input_box.setBordered_(False)
        input_box.setDrawsBackground_(True)
        input_box.setBackgroundColor_(NSColor.colorWithCalibratedWhite_alpha_(0.2, 1.0))
        input_box.setEditable_(True)
        input_box.setSelectable_(True)
        input_box.setFocusRingType_(1)

        content.addSubview_(input_box)
        content.input_box = input_box

        # Critical: make window key and give responder to text field
        window.makeKeyAndOrderFront_(None)
        window.makeFirstResponder_(input_box)

        # Push label up
        for subview in content.subviews():
            if isinstance(subview, NSTextField) and subview != input_box:
                subframe = subview.frame()
                subframe.origin.y = input_y + input_height + 10
                subview.setFrame_(subframe)

    else:
        # ---- COLLAPSE ----
        if hasattr(content, "input_box"):
            content.input_box.removeFromSuperview()
            delattr(content, "input_box")

        # Pull label back down
        for subview in content.subviews():
            if isinstance(subview, NSTextField):
                subframe = subview.frame()
                subframe.origin.y = 10
                subview.setFrame_(subframe)

    expanded = not expanded
