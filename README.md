

# Event Registration Bot

This bot automates the registration process for events on a website by clicking through the necessary steps until checkout. **It requires you to manually log in and register a card first.**

---

## Features

* Automatically clicks through event registration steps.
* Uses the first saved card on your account for checkout.
* Stops before final checkout so you can verify everything.

---

## Prerequisites

* [Python 3.x](https://www.python.org/downloads/)
* [Google Chrome](https://www.google.com/chrome/)
* [Visual Studio Code](https://code.visualstudio.com/)

---

## Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. **Install required packages**
   Run this in your terminal (Command Prompt or VS Code terminal):

```bash
pip install -r requirements.txt
```

---

## Setup

1. **Log in manually**

   * Open Chrome and log in to your account.
   * Register a payment card if you haven’t already.
   * The **first card** on file will be used by the bot.

2. **Navigate to the event page**

   * Go to the specific event you want to register for.
   * Keep this page open in Chrome.

3. **Start Chrome with remote debugging**

```bash
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selprofile"
```

> Make sure the path to Chrome matches your system.

---

## Running the Bot

1. Open Visual Studio Code.
2. Open the folder containing the bot scripts.
3. Open the **main Python file** (e.g., `bot.py`).
4. Run the file using the top “Run Python File” button in VS Code.

The bot will:

* Refresh the page until the event opens.
* Click through the steps automatically.
* Stop right before the final checkout for manual verification.

---

## Notes

* Make sure your first saved card is the one you want the bot to use.
* Do not close the Chrome window while the bot is running.
* The bot is intended for personal use. Use responsibly.

---

## Useful Links

* [Visual Studio Code](https://code.visualstudio.com/)
* [Python Download](https://www.python.org/downloads/)
* [Google Chrome Download](https://www.google.com/chrome/)

---

If you want, I can also **add a “How it works” diagram** showing the sequence of steps the bot clicks, which makes the README much more user-friendly.

Do you want me to include that?
