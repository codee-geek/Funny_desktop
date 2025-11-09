# Funny Desktop Roaster (Fun Roast Overlay)

A lightweight macOS utility that observes your active app or browser tab and generates short, 
sarcastic roasts based on what you're doing. Runs fully offline using a local LLM with no API cost.

---

## Features
- Detects the currently focused app and active browser URL.
- Classifies activity into simple context labels (e.g., browsing, coding, ChatGPT, etc.).
- Generates a one-line roast using a local Phi-3 Mini LLM.
- Displays the roast live through a macOS menu bar overlay.
- Works completely offline. No external API calls.

---

## System Architecture

get_active_app_info → classify context → generate roast → display in overlay

---


| Component | Responsibility |
|----------|----------------|
| `detect_screen.py` | Detects current app and window title. Retrieves browser URL when applicable. |
| `context_map.py` | Converts raw app/window data into semantic context (e.g., "doomscrolling YouTube"). |
| `roaster.py` | Uses local Phi-3 model to generate sarcastic one-liner roast. |
| `tray.py` | Displays roast in macOS menu bar and updates periodically. |
| `main.py` | Core loop that glues everything together. |

---

## Model

The project uses **Phi-3 Mini 4K Instruct** in **GGUF** format:

---

## Setup
1. Clone the repo
2. Create venv and install dependencies:
   pip install -r requirements.txt
3. Download the model file:
   https://huggingface.co/bartowski/Phi-3-mini-4k-instruct-GGUF/tree/main
   File: phi-3-mini-4k-instruct-IQ4_NL.gguf
4. Place the downloaded .gguf file in the project folder:
   funny01/ 
