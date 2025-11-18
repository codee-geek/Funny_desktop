def classify(app, title, url=None):
    """
    Classify user activity into a semantic context for roasting.
    
    Args:
        app: Application name
        title: Window title
        url: Browser URL (if applicable)
    
    Returns:
        String describing the user's activity context
    """
    if not app:
        return "doing absolutely nothing"
    
    app_lower = app.lower()
    title_lower = (title or "").lower()
    url_lower = (url or "").lower() if url else ""

    # Known browser contexts (check URL first for specificity)
    browsers = ("chrome", "safari", "firefox", "brave", "edge")
    if any(browser in app_lower for browser in browsers):
        if "youtube.com" in url_lower or "youtu.be" in url_lower:
            return "watching YouTube instead of working"
        if "github.com" in url_lower:
            return "pretending to improve code"
        if "chatgpt.com" in url_lower or "openai.com" in url_lower or "claude.ai" in url_lower:
            return "outsourcing thinking to an AI"
        if "netflix.com" in url_lower or "hulu.com" in url_lower or "disney+" in url_lower:
            return "full recreational mode"
        if "reddit.com" in url_lower:
            return "doomscrolling Reddit"
        if "twitter.com" in url_lower or "x.com" in url_lower:
            return "wasting time on Twitter"
        if "instagram.com" in url_lower:
            return "comparing life to fake highlights"
        return "aimlessly browsing the internet"

    # Coding environments
    coding_apps = ("code", "vscode", "visual studio", "xcode", "pycharm", "intellij", "sublime")
    if any(coding_app in app_lower for coding_app in coding_apps):
        return "staring at code hoping it fixes itself"

    # Notes / docs
    if "notes" in app_lower or "obsidian" in app_lower or "notion" in app_lower:
        return "writing ideas you will probably ignore"

    # Messaging
    messaging_apps = ("whatsapp", "teams", "discord", "slack", "messages", "telegram")
    if any(msg_app in app_lower for msg_app in messaging_apps):
        return "trying to look social but avoiding real conversations"

    # Terminal/CLI
    if "terminal" in app_lower or "iterm" in app_lower or "zsh" in app_lower or "bash" in app_lower:
        return "pretending to be a hacker in terminal"

    # Fallback
    return f"using {app} with no clear intent"
