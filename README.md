# MinecraftRealmsDiscordBot

## What is this?

This is the Discord bot that notify who are online on the Mincraft Realms.

## How to use?

- Clone this repository
- I recommend to use `pyenv`
  - https://github.com/pyenv/pyenv
- Install Python 3.8.6
  - `pyenv install 3.8.6`
- Install `requirements.txt`
  - `pip install -r requirements.txt`
- Setup `.env`
- Run `python main.py`

You must add `.env` file and put the following environment variables:

- `OPENXBL_TOKEN`
  - This bot fetch info via OpenXBL, an unofficial Xbox Live API.
  - https://xbl.io/
  - You should LOGIN to OpenXBL by your Microsoft Account and create API Key.
  - Dont forget to memo API Key, You can only see it when it's created.
- `REALMS_CLUB_ID`
  - When you create the Mincraft Realms, Microsoft automatically and implicitly creates the 'Club' in Xbox Live.
  - You can find the 'Club' that one-to-one pair of your Minecraft Realms at URL below:
  - https://account.xbox.com/Profile?xr=mebarnav
- `DISCORD_WEBHOOK`
  - Of course, this is Discord bot, so you should create Webhook for your Discord server.
  - Webhook instructions is covered Discord official support document:
  - https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

## How to contribute?

TBD
