# 🖥️ PC Control Telegram Bot

An asynchronous Telegram bot built with **Aiogram 3**, designed for remote monitoring and control of a Windows-based PC/laptop.

## ✨ Features

* **📊 System Status:** View current CPU and RAM usage, as well as battery status.
* **📋 Clipboard:** Quickly read the current text from the PC's clipboard (with automatic escaping and length limits to prevent Telegram API errors) + the `/set` command to remotely send text to the clipboard.
* **🎵 Media Controller:** A convenient Inline keyboard to skip tracks, change volume, and play/pause (simulating media keys).
* **⚙️ Heavy Processes:** Displays the Top 5 processes consuming the most RAM, with the ability to completely terminate (kill) a process tree by its PID using the `/kill PID` command.
* **💤 Sleep Mode & 🛑 Shutdown:** Remotely put the device to sleep or shut it down completely.
* **🔒 Security:** The bot responds exclusively to the administrator's commands (specified by `ADMIN_ID`). Requests from other users are completely ignored.

---

## 🛠️ Requirements & Installation

### 1. Clone the repository
```bash
git clone https://github.com/clowdyyy/pc-control.git
cd pc-control
```

### 2. Install dependencies
The script requires specific modules to interact with the system. Install them using a single command:
```bash
pip install -r requirements.txt
```

### 3. Environment setup
Rename the demo `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Open the created `.env` file and fill in your configuration data:
* `BOT_TOKEN` — your bot token from `@BotFather`.
* `ADMIN_ID` — your numeric Telegram ID (can be obtained via `@userinfobot`).

---

## 🚀 Launch

Run the script using the standard Python command:
```bash
python main.py
```
After launching, go to Telegram and send the `/start` command to the bot.

## ⚙️ Autostart (Background Mode for Windows)

To make the bot run silently in the background every time your PC starts, you can use a VBScript.

1. Press `Win + R`, type `shell:startup`, and press **Enter**.
2. Create a new file named `run_bot.vbs` in the opened folder.
3. Paste the following code into the file (replace the path with your actual absolute path to the project directory):

```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Path\To\Your\pc-control"
WshShell.Run "python main.py", 0, false
```
4. Save the file. The bot will now automatically start in the background upon booting Windows.

---

## ⚠️ Important Note
The `.env` configuration file contains sensitive data (your bot token) and is automatically added to `.gitignore`. Never publish it in the public domain.