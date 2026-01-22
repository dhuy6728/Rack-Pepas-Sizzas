"""
Discord Bot - Main File
"""
import discord
from discord.ext import commands
import logging
import os
from config import DISCORD_TOKEN, BOT_PREFIX, BOT_STATUS, LOG_LEVEL, LOG_FORMAT, LOG_FILE

# Thiết lập logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create bot with required intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    """Event called when the bot is ready"""
    logger.info(f'{bot.user} has connected!')
    
    # Set bot activity/status
    await bot.change_presence(
        activity=discord.Game(name=BOT_STATUS)
    )

@bot.event
async def on_message(message):
    """Event called when a new message is received"""
    # Ignore messages from bot
    if message.author == bot.user:
        return
    
    logger.info(f'{message.author} ({message.author.id}): {message.content}')
    
    # Process commands
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    logger.error(f'Error in command {ctx.command}: {error}')
    await ctx.send(f'❌ Error: {error}')

# ==================== COMMANDS ====================

@bot.command(name='ping', help='Check bot latency')
async def ping(ctx):
    """Ping command - check latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latency: {latency}ms')

@bot.command(name='hello', help='Bot will greet you')
async def hello(ctx):
    """Hello command - bot greets you"""
    await ctx.send(f'👋 Hello {ctx.author.mention}!')

@bot.command(name='user', help='Display user information')
async def user_info(ctx, user: discord.User = None):
    """User command - display user information"""
    if user is None:
        user = ctx.author
    
    embed = discord.Embed(
        title=f'Information about {user.name}',
        color=discord.Color.blue()
    )
    embed.add_field(name='User ID', value=user.id, inline=False)
    embed.add_field(name='Account Created', value=user.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=False)
    embed.set_thumbnail(url=user.display_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name='help_custom', help='Display list of commands')
async def help_custom(ctx):
    """Display list of custom commands"""
    embed = discord.Embed(
        title='📚 Command List',
        description='All available commands:',
        color=discord.Color.green()
    )
    
    commands_list = [
        ('!ping', 'Check bot latency'),
        ('!hello', 'Bot will greet you'),
        ('!user [@user]', 'Display user information'),
        ('!rps @opponent', '🎲 Play Rock Paper Scissors Multiplayer (2 players)'),
        ('!rpshelp', '📖 View RPS game guide'),
        ('!help_custom', 'Display command list'),
    ]
    
    for cmd, desc in commands_list:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    await ctx.send(embed=embed)

# ==================== LOAD COGS ====================

async def load_cogs():
    """Load all cogs from cogs directory"""
    cogs_dir = 'cogs'
    if os.path.exists(cogs_dir):
        for filename in os.listdir(cogs_dir):
            if filename.endswith('.py'):
                cog_name = filename[:-3]
                try:
                    await bot.load_extension(f'cogs.{cog_name}')
                    logger.info(f'Cog {cog_name} has been loaded')
                except Exception as e:
                    logger.error(f'Error loading cog {cog_name}: {e}')

async def main():
    """Main function"""
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

# Run bot
if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot has stopped')
