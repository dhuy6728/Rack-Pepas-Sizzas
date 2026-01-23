# Simple Discord Bot 🤖

A Discord Bot built with Python using the `discord.py` library.

## Features

✨ **Basic Commands:**
- `!ping` - Check bot latency
- `!hello` - Bot will greet you
- `!user [@user]` - Display user information
- `!help` - Display all commands list

🎮 **Fun Commands:**
- `!dice` - Roll a 6-sided dice
- `!coin` - Flip a coin
- `!cf` or `!coinflip` - Flip a coin (shortcut)
- `!random [min] [max]` - Pick a random number
- `!choose [option1] [option2] ...` - Choose a random option
- `!diceroll` or `!dr` - Roll 1, 2, or 3 dice with button interface

🎲 **Rock Paper Scissors Multiplayer:**
- `!rps @opponent` - Play Rock Paper Scissors with another player (2 players)
  - Use in-channel buttons to choose (hidden confirmations)
  - Click ✊ 📄 ✂️ to select your move
  - Result shows when both choose or after 30 seconds
  - If only 1 person chooses = they lose
- `!rpsbot` or `!rpsbot [1/2/3]` - Play against the bot (single-player)
- `!rpshelp` - View detailed RPS guide

🔨 **Moderation Commands:**
- `!kick [@member] [reason]` - Kick a member (requires permissions)
- `!ban [@member] [reason]` - Ban a member (requires permissions)
- `!mute [@member]` - Mute a member (requires permissions)
- `!clear [amount]` - Clear messages (requires permissions)

## Requirements

- Python 3.8+
- pip (Package installer for Python)

## Installation

### 1. Clone or download the project

```bash
cd "d:\Python Project\Discord Bot"
```

### 2. Create Virtual Environment (optional but recommended)

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

Copy `.env.example` and rename it to `.env`:

```bash
cp .env.example .env
```

Or create `.env` manually and add:

```
DISCORD_TOKEN=your_bot_token_here
BOT_PREFIX=!
BOT_STATUS=Hello World!
```

### 5. Get Your Bot Token

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a "New Application"
3. Name your bot
4. Go to "Bot" tab and click "Add Bot"
5. Copy the token and paste it in `.env`
6. Enable required intents:
   - SERVER MEMBERS INTENT
   - MESSAGE CONTENT INTENT

### 6. Add bot to your server

1. Go to "OAuth2" → "URL Generator"
2. Select scope: `bot`
3. Select required permissions (Send Messages, Manage Messages, etc.)
4. Copy the generated URL and open in browser
5. Select server and add the bot

## Running the Bot

```bash
python main.py
```

You should see:
```
2024-XX-XX XX:XX:XX,XXX - __main__ - INFO - YourBotName#0000 has connected!
```

The bot is ready!

## Project Structure

```
Discord Bot/
├── main.py                 # Main bot file
├── config.py               # Configuration file
├── requirements.txt        # Required packages list
├── .env.example           # .env template
├── .gitignore             # Git ignore file
├── README.md              # This file
├── cogs/                  # Feature modules
│   ├── fun.py             # Fun commands
│   ├── moderation.py      # Moderation commands
│   └── rps.py             # Rock Paper Scissors game
└── logs/                  # Log directory
```

## Creating a New Cog (Module)

To add new commands, create a new file in the `cogs/` directory:

```python
import discord
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='mycommand', help='Command description')
    async def my_command(self, ctx):
        await ctx.send('Hello!')

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

Save the file and the bot will automatically load it!

## Troubleshooting

### Bot not connecting
- Check token in `.env`
- Verify bot is added to server
- Check intents are enabled in Developer Portal

### Commands not working
- Verify prefix (default is `!`)
- Check bot has required permissions
- Check logs for errors

### Module not loading
- Check file name in `cogs/` directory
- Verify file syntax

## Useful Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/)
- [Discord Permissions Calculator](https://discordapi.com/permissions.html)

## Deployment (24/7 Uptime)

Deploy to Railway for free 24/7 hosting:

1. Push code to GitHub (see `QUICKSTART.md`)
2. Go to https://railway.app
3. Create new project and select GitHub repo
4. Add `DISCORD_TOKEN` environment variable
5. Deploy - bot runs 24/7!

## License

MIT License

## Support

If you have questions or encounter issues, please open an issue!

---

**Happy bot building!** 🚀
