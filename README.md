# TeleWhisper - Public Release

Public version of the TeleWhisper project.

This Telegram bot is able to, in private chat with it, transcribe audios, videos, music, etc. to text, and send it back to you.

Structure may be a bit messy, as it was not intended to be public, but it works as intended. Feel free to use it, modify it, and do whatever you want with it as long as you follow the [license](#license).

## Table of contents
- [How it works](#how-it-works)
- [How to use](#how-to-use)
  - [Using the bot](#using-the-bot)
  - [Running your own bot](#running-your-own-bot)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Running it locally](#running-it-locally)
    - [Using a VPS](#using-a-vps)

- [Learn more](#learn-more)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)


## How it works

This bot uses [OpenAIs whisper model]([Title](https://github.com/openai/whisper)) in order to get the trasncription from any multimedia file. It also uses the [Telegram Bot API](https://core.telegram.org/bots/api) to interact with the user. In order to connect to the API, it uses the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library.

You can head out to the [Wiki](https://github.com/FosanzDev/TeleWhisperPublic/wiki) to learn more about the files and how they work.

# How to use
### Using the bot
---
Get in Telegram and search for `@TeleWhisperBot`, or click [here](https://t.me/TeleWhisperBot). Click on `START` button to start using it. Then send any audio, video, music, etc. to it, and it will send you back the transcription.

### Running your own bot
---
### *Requirements*

- Python 3.6 or higher
- [FFmpeg](https://ffmpeg.org/) installed and added to PATH:
    - Windows: [Download](https://www.gyan.dev/ffmpeg/builds/)
    - Linux: `sudo apt install ffmpeg`

- A Telegram bot token. You can get one by talking to [@BotFather](https://t.me/BotFather) in Telegram.
- An OpenAI API key. You can get one by signing up [here](https://platform.openai.com/account/api-keys).
- (optional) A payment token. You can get it also by talking to [@BotFather](https://t.me/BotFather) in Telegram.
If you're not planning on using the `/tip` command, you should remove it from the code. Head to the [Wiki](https://github.com/FosanzDev/TeleWhisperPublic/wiki) to learn how to do it.

---
### *Installation*

#### 1. Clone the repository:
```bash	
git clone https://github.com/FosanzDev/TeleWhisperPublic.git
```

#### 2. Install the requirements:
```bash
pip install -r requirements.txt
```

#### 3. Install ffmpeg:
- Windows: [Download](https://www.gyan.dev/ffmpeg/builds/)
- Linux: `sudo apt install ffmpeg`

#### 4. Insert the API keys in the `keyHolder.py` file:
```python
telegramApiKey = '...'
openaiApiKey = '...'
paymentProcessorApiKey = '...'
```

---

### *Running it locally*

You can run it locally by running the `telegramListener.py` file:
```bash
python3 telegramListener.py
```

This will start the bot, and you will be able to use it in Telegram. If you want to stop it, just press `CTRL + C` in the terminal.

You can also set up a Raspberry Pi to run it 24/7. You can follow the steps shown in [Using a VPS](#using-a-vps) to do so.


---

### *Using a VPS*

For this bot, a VPS is recommended, as it will be running 24/7. You can use any VPS provider you want, but I recommend [IONOS 1&1](https://www.ionos.es/servidores/vps) (This is the spanish version of the page since it's cheaper than the US one). Personally a VPS with 1 vCore and 1GB of RAM is way more than enough, but you can use more if you want.

Make sure it runs python 3.6 or higher, and that you have installed ffmpeg. Recommended OS is Ubuntu 20.04. Tutorial will be based on this OS and version.

#### 1. Connect to the VPS via SSH. I recommend using [Termius](https://termius.com/) since it's free and multiplatform.

#### 2. Clone the repo, install the requirements and ffmpeg as shown in [Installation](#installation).

#### 3. Insert the API keys in the `keyHolder.py` file as shown in [Installation](#installation).

#### 4. Run the bot:
```bash
python3 telegramListener.py & disown
# Using disown will make the process run in the background, so you can close the SSH session without stopping the bot.
```

#### 5. Make it a service (optional):
First, create an script that will run the bot:
```bash
nano runBot.sh
```
Then, insert the following code:
```bash
#!/bin/bash
cd /path/to/the/repo
git pull --force # This will make sure the bot is always up to date
python3 telegramListener.py
```
Save the file and exit the editor.

Now, create a service file:
```bash
sudo nano /etc/systemd/system/telewhisper.service
```

And insert the following code:
```bash
[Unit]
Description=TeleWhisper Bot

[Service]
ExecStart=/path/to/the/script/runBot.sh

[Install]
WantedBy=multi-user.target
```

Save the systemctl config:
```bash
sudo systemctl reload
```

And enable the service:
```bash
sudo systemctl enable telewhisper.service
```


This will make the bot run as a service, so it will start automatically when the VPS boots up. You can also start/stop/restart the bot with the following commands:
```bash
sudo systemctl start telewhisper
sudo systemctl stop telewhisper
sudo systemctl restart telewhisper
```

---

## Learn more

- You can head out to the [Wiki](https://github.com/FosanzDev/TeleWhisperPublic/wiki) to learn more about the files and how they work.

- You can also check out the [Telegram Bot API](https://core.telegram.org/bots/api) and the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library to learn more about how the bot works.

- You can also check out the [OpenAI API](https://beta.openai.com/docs/api-reference) to learn more about how the transcription works.

- You can also check out the [OpenAI whisper model](https://github.com/openai/whisper) to learn deeper about how the transcription works.

---
## License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.

---

## Contributing

You can contribute to this project by forking it and making a pull request. You can also contact me via Telegram [@Fosanz](https://t.me/Fosanz). 

You can contribute economically by donating to the following addresses:
- PayPal: [paypal.me/fosanzdev](https://paypal.me/fosanzdev)
- BuyMeACoffee: [Fosanzdev](https://www.buymeacoffee.com/fosanzdev)

---

## Contact
Any questions, suggestions or issues, you can contact me via Telegram [@Fosanz](https://t.me/Fosanz) or by sending an email to [fosanzdev@gmail.com](mailto:fosanzdev@gmail.com)