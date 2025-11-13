from Foundation import NSRect

expanded = False

def toggle_overlay_expansion(window):
    """Toggle overlay expansion with animation"""
    global expanded
    frame = window.frame()
    w = frame.size.width
    x = frame.origin.x
    y = frame.origin.y
    new_h = 200 if not expanded else 50
    new_rect = NSRect((x, y), (w, new_h))
    window.setFrame_display_animate_(new_rect, True, True)
    expanded = not expanded
