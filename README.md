# TelegramGPT

A [gpt4free](https://github.com/xtekky/gpt4free) integration for Telegram

## Info

This project uses the gpt4free modules to interact with third party AI assistants from a Telegram Bot

## Uasge

1. Define the `BOT_TOKEN` environment variable by setting the value of your bot API token
2. Clone the gpt4free repo and move the `g4f` folder in the same dir as the `main.py` script
3. Install dependencies from the `g4f` repo
4. Install dependencies from this repo
5. Execute `main.py`

## Whitelist

This tools uses some third parties API(s) that may report an overload if the bot is processing too much input, to avoid this, you can specify a whitelist by creating a `BOT_WHITELIST` environment variable which contains a list of comma-separated CHAT ID(s) that can access your bot

## Admin configuration

An administrator account can be set in the environment variable `BOT_ADMIN` to receive alerts if needed