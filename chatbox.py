from Foundation import NSRect, NSObject, NSMutableAttributedString, NSAttributedString
from AppKit import (
    NSTextField,
    NSColor,
    NSFont,
    NSView,
    NSMutableParagraphStyle,
    NSFontAttributeName,
    NSForegroundColorAttributeName,
    NSParagraphStyleAttributeName,
    NSTextAlignmentRight,
    NSTextAlignmentLeft,
)
import objc
import threading
import db
import roaster

expanded = False


def process_user_reply(user_message):
    """Process user reply and generate a response."""
    try:
        if not user_message or not user_message.strip():
            print("[DEBUG] Empty message, skipping")
            return
        
        user_msg = user_message.strip()
        print(f"[DEBUG] Processing user reply: '{user_msg}'")
        
        # Store user message in database
        print(f"[DEBUG] Storing user message in DB...")
        db.insert_message("user", user_msg)
        print(f"[DEBUG] User message stored")
        
        # Generate a roast response based on user's message
        # Use conversation context for better responses
        print(f"[DEBUG] Getting recent messages...")
        recent_messages = db.get_recent_messages(limit=5)
        context = f"User said: {user_msg}"
        
        # Generate response
        print(f"[DEBUG] Generating roast reply...")
        response = roaster.roast_reply(context, recent_messages)
        print(f"[DEBUG] Got response: '{response}'")
        
        # Store response in database
        print(f"[DEBUG] Storing response in DB...")
        db.insert_message("roaster", response)
        print(f"[DEBUG] Response stored")
        
        # Update overlay/chat with response
        handle_roast_display(response)
        print(f"[SUCCESS] User: {user_msg}")
        print(f"[SUCCESS] Roaster: {response}")
        
        refresh_conversation_if_visible()
    except Exception as e:
        print(f"[ERROR] Error processing user reply: {e}")
        import traceback
        traceback.print_exc()


class TextFieldDelegate(NSObject):
    """Delegate to handle Enter key in text field."""
    
    def control_textView_doCommandBySelector_(self, control, textView, commandSelector):
        """Handle command selectors like insertNewline (Return key)."""
        try:
            # Get selector name - PyObjC uses different methods
            from AppKit import NSSelectorFromString
            selector_name = str(commandSelector)
            print(f"[DEBUG] Delegate called with selector: {selector_name}")
            
            # Check for newline commands
            if "insertNewline" in selector_name or "insertLineBreak" in selector_name or "insertParagraphSeparator" in selector_name:
                text = control.stringValue()
                print(f"[DEBUG] Enter/Return pressed via delegate, text: '{text}'")
                if text and text.strip():
                    text_to_send = text.strip()
                    print(f"[DEBUG] Processing reply: '{text_to_send}'")
                    # Process reply in background thread to avoid blocking UI
                    threading.Thread(
                        target=process_user_reply,
                        args=(text_to_send,),
                        daemon=True
                    ).start()
                control.setStringValue_("")
                return True  # We handled it, don't do default behavior
        except Exception as e:
            print(f"[ERROR] Delegate error: {e}")
            import traceback
            traceback.print_exc()
        return False  # Let default behavior happen for other commands


class ReplyField(NSTextField):
    """Custom text field for user replies."""
    
    def acceptsFirstResponder(self):
        return True

    def becomeFirstResponder(self):
        result = objc.super(ReplyField, self).becomeFirstResponder()
        print(f"[DEBUG] ReplyField became first responder: {result}")
        return result
    
    def awakeFromNib(self):
        """Called when field is created."""
        objc.super(ReplyField, self).awakeFromNib()
        print("[DEBUG] ReplyField awakeFromNib called")
    
    def keyDown_(self, event):
        try:
            key_code = event.keyCode()
            print(f"[DEBUG] Key pressed in ReplyField: code={key_code}, chars='{event.characters()}'")
            # Key codes: 36 = Return, 76 = Enter (numeric keypad), 13 = Enter (some keyboards)
            if key_code == 36 or key_code == 76 or key_code == 13:
                text = self.stringValue()
                print(f"[DEBUG] Enter pressed in keyDown_, text: '{text}'")
                if text and text.strip():
                    text_to_send = text.strip()
                    print(f"[DEBUG] Processing reply from keyDown_: '{text_to_send}'")
                    # Process reply in background thread to avoid blocking UI
                    threading.Thread(
                        target=process_user_reply,
                        args=(text_to_send,),
                        daemon=True
                    ).start()
                self.setStringValue_("")
                # Don't call super to prevent default behavior
                return
        except Exception as e:
            print(f"[ERROR] keyDown_ error: {e}")
            import traceback
            traceback.print_exc()
        objc.super(ReplyField, self).keyDown_(event)


def update_conversation_display(conversation_label):
    """Update the conversation display with recent messages."""
    try:
        recent_messages = db.get_recent_messages(limit=10)
        if not recent_messages:
            placeholder = NSAttributedString.alloc().initWithString_attributes_(
                "No comebacks yet. Be the first to clap back.",
                {
                    NSFontAttributeName: NSFont.systemFontOfSize_(12),
                    NSForegroundColorAttributeName: NSColor.colorWithCalibratedWhite_alpha_(0.8, 1.0),
                },
            )
            conversation_label.setAttributedStringValue_(placeholder)
            return

        styled = NSMutableAttributedString.alloc().init()

        for role, message, timestamp in recent_messages:
            para = NSMutableParagraphStyle.alloc().init()
            if role == "user":
                para.setAlignment_(NSTextAlignmentRight)
                bubble_color = NSColor.systemTealColor()
                label = "You"
            else:
                para.setAlignment_(NSTextAlignmentLeft)
                bubble_color = NSColor.systemOrangeColor()
                label = "Roaster"

            para.setParagraphSpacing_(4)
            para.setLineHeightMultiple_(1.2)

            font = NSFont.systemFontOfSize_(12)
            line = f"{label}: {message}"

            attrs = {
                NSFontAttributeName: font,
                NSForegroundColorAttributeName: bubble_color,
                NSParagraphStyleAttributeName: para,
            }

            snippet = NSAttributedString.alloc().initWithString_attributes_(line + "\n", attrs)
            styled.appendAttributedString_(snippet)

        conversation_label.setAttributedStringValue_(styled)
    except Exception as e:
        print(f"[ERROR] Error updating conversation display: {e}")


def refresh_conversation_if_visible():
    """Convenience helper to redraw the chat conversation if it exists."""
    try:
        import overlay

        if overlay.window and overlay.window.contentView():
            content = overlay.window.contentView()
            if hasattr(content, "conversation_label"):
                update_conversation_display(content.conversation_label)
    except Exception as e:
        print(f"[ERROR] Unable to refresh conversation view: {e}")


def handle_roast_display(latest_roast):
    """Show roasts either in the overlay label or inside the chat console."""
    try:
        import overlay
    except ImportError:
        return

    content = overlay.window.contentView() if overlay.window else None

    if expanded and content:
        roast_label = getattr(content, "roast_label", None)
        if roast_label:
            roast_label.setHidden_(True)
        refresh_conversation_if_visible()
    else:
        overlay.last_roast = latest_roast
        if content:
            roast_label = getattr(content, "roast_label", None)
            if roast_label:
                roast_label.setHidden_(False)


def toggle_overlay_expansion(window, roast_label=None):
    """Expand or collapse overlay with input box."""
    global expanded

    frame = window.frame()
    w = frame.size.width
    x = frame.origin.x
    y = frame.origin.y
    
    expanded = not expanded
    new_h = 340 if expanded else 60
    new_rect = NSRect((x, y), (w, new_h))
    window.setFrame_display_animate_(new_rect, True, True)

    content = window.contentView()
    content_width = w - 24  # margin * 2

    # Ensure main label stays anchored near the top edge
    label_ref = roast_label or getattr(window.contentView(), "roast_label", None)
    if label_ref is not None:
        label_frame = label_ref.frame()
        if expanded:
            label_frame.origin.y = new_h - label_frame.size.height - 12
        else:
            label_frame.origin.y = 10
        label_ref.setFrame_(label_frame)
        label_ref.setHidden_(expanded)

    # Communicate chat state back to overlay for other components.
    try:
        import overlay

        overlay.chat_active = expanded
    except Exception:
        pass

    if expanded:
        # ---- EXPAND ----
        outer_margin = 12
        chat_height = new_h - 80

        chat_container = NSView.alloc().initWithFrame_(
            NSRect((outer_margin, outer_margin), (content_width, chat_height))
        )
        chat_container.setWantsLayer_(True)
        chat_layer = chat_container.layer()
        chat_layer.setCornerRadius_(16)
        chat_layer.setMasksToBounds_(True)
        chat_layer.setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(0.12, 0.13, 0.17, 0.92).CGColor())

        content.addSubview_(chat_container)
        content.chat_container = chat_container

        input_height = 36
        inner_margin = 12
        chat_width = chat_container.frame().size.width
        header_height = 20

        conv_height = (
            chat_container.frame().size.height
            - input_height
            - header_height
            - (inner_margin * 4)
        )
        conversation_label = NSTextField.alloc().initWithFrame_(
            NSRect(
                (inner_margin, inner_margin * 2 + input_height),
                (chat_width - 2 * inner_margin, conv_height),
            )
        )
        conversation_label.setFont_(NSFont.systemFontOfSize_(12))
        conversation_label.setAllowsEditingTextAttributes_(True)
        conversation_label.setTextColor_(NSColor.colorWithCalibratedWhite_alpha_(0.95, 1.0))
        conversation_label.setBezeled_(False)
        conversation_label.setBordered_(False)
        conversation_label.setDrawsBackground_(False)
        conversation_label.setEditable_(False)
        conversation_label.setSelectable_(True)
        conversation_label.setAlignment_(0)
        conversation_label.cell().setWraps_(True)
        conversation_label.cell().setUsesSingleLineMode_(False)
        chat_container.addSubview_(conversation_label)
        content.conversation_label = conversation_label

        update_conversation_display(conversation_label)
        header_label = NSTextField.alloc().initWithFrame_(
            NSRect(
                (inner_margin, chat_container.frame().size.height - header_height - inner_margin),
                (chat_width - 2 * inner_margin, header_height),
            )
        )
        header_label.setStringValue_("Clapback Console")
        header_label.setFont_(NSFont.boldSystemFontOfSize_(13))
        header_label.setTextColor_(NSColor.whiteColor())
        header_label.setBezeled_(False)
        header_label.setBordered_(False)
        header_label.setDrawsBackground_(False)
        header_label.setEditable_(False)
        header_label.setSelectable_(False)
        chat_container.addSubview_(header_label)
        content.header_label = header_label

        input_box = ReplyField.alloc().initWithFrame_(
            NSRect((inner_margin, inner_margin),
                   (chat_width - 2 * inner_margin, input_height))
        )
        input_box.setPlaceholderString_("Drop your comeback...")
        input_box.setFont_(NSFont.systemFontOfSize_(13))
        input_box.setTextColor_(NSColor.whiteColor())
        input_box.setBezeled_(False)
        input_box.setBordered_(False)
        input_box.setDrawsBackground_(True)
        input_box.setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(0.33, 0.35, 0.9, 0.35))
        input_box.setEditable_(True)
        input_box.setSelectable_(True)
        input_box.setFocusRingType_(1)
        input_box.setAlignment_(0)

        delegate = TextFieldDelegate.alloc().init()
        input_box.setDelegate_(delegate)
        chat_container.addSubview_(input_box)

        content.input_box = input_box
        content.input_delegate = delegate

        window.makeKeyAndOrderFront_(None)
        window.makeFirstResponder_(input_box)
        print("[DEBUG] Overlay expanded with chat container")

    else:
        # ---- COLLAPSE ----
        if hasattr(content, "input_box"):
            content.input_box.removeFromSuperview()
            delattr(content, "input_box")
        if hasattr(content, "conversation_label"):
            content.conversation_label.removeFromSuperview()
            delattr(content, "conversation_label")
        if hasattr(content, "chat_container"):
            content.chat_container.removeFromSuperview()
            delattr(content, "chat_container")
        if hasattr(content, "header_label"):
            content.header_label.removeFromSuperview()
            delattr(content, "header_label")
        if hasattr(content, "input_delegate"):
            delattr(content, "input_delegate")

        print("[DEBUG] Overlay collapsed")
