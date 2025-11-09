def classify(app, title, url=None):
    app = app.lower()
    title = (title or "").lower()
    url = (url or "").lower() if url else ""

    # Known browser contexts
    if "chrome" in app or "safari" in app or "firefox" in app:
        if "youtube.com" in url:
            return "watching YouTube instead of working"
        if "github.com" in url:
            return "pretending to improve code"
        if "chatgpt.com" in url or "openai.com" in url:
            return "outsourcing thinking to an AI"
        if "netflix.com" in url:
            return "full recreational mode"
        return "aimlessly browsing the internet"

    # Coding
    if "code" in app or "vscode" in app or "visual studio" in app:
        return "staring at code hoping it fixes itself"

    # Notes / docs
    if "notes" in app or "obsidian" in app:
        return "writing ideas you will probably ignore"

    # Messaging
    if "whatsapp" in app or "teams" in app or "discord" in app:
        return "trying to look social but avoiding real conversations"

    # Fallback
    return f"using {app} with no clear intent"
