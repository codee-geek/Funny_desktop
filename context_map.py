def classify(app, title):
    app = app.lower()
    title = title.lower()

    if "colab" in title:
        return "working on Colab but avoiding actually running code"

    if "chatgpt" in app or "openai" in title:
        return "asking an AI to solve life"

    if "code" in app or "vscode" in app or "visual studio" in app:
        return "staring at code hoping it fixes itself"

    if "chrome" in app or "safari" in app or "firefox" in app:
        if "youtube" in title:
            return "watching YouTube instead of doing work"
        if "github" in title:
            return "browsing GitHub pretending to improve"
        return "aimlessly browsing the internet"

    return f"using {app} with title: {title}"
