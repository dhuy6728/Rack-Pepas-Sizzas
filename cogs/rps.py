"""
Cog - Rock Paper Scissors Multiplayer
2-player game with hidden choices
"""
import discord
from discord.ext import commands
import asyncio
from enum import Enum
from typing import Dict, Optional
import random

class Choice(Enum):
    """Game choices"""
    ROCK = "✊ Rock"
    PAPER = "📄 Paper"
    SCISSORS = "✂️ Scissors"

class RPSGame:
    """Class to manage a Rock Paper Scissors game"""
    
    def __init__(self, player1: discord.Member, player2: discord.Member, channel: discord.TextChannel):
        self.player1 = player1
        self.player2 = player2
        self.channel = channel
        
        self.choice1: Optional[Choice] = None
        self.choice2: Optional[Choice] = None
        
        self.game_message: Optional[discord.Message] = None
        self.status_message: Optional[discord.Message] = None
    # In-channel flow will be used; choices are collected via a shared View
    
    def get_opponent(self, player: discord.Member) -> discord.Member:
        """Get opponent of a player"""
        return self.player2 if player.id == self.player1.id else self.player1
    
    def set_choice(self, player: discord.Member, choice: Choice) -> bool:
        """Set choice for a player"""
        if player.id == self.player1.id:
            if self.choice1 is not None:
                return False
            self.choice1 = choice
            return True
        elif player.id == self.player2.id:
            if self.choice2 is not None:
                return False
            self.choice2 = choice
            return True
        return False
    
    def is_complete(self) -> bool:
        """Check if both players have chosen"""
        return self.choice1 is not None and self.choice2 is not None
    
    def get_result(self) -> tuple:
        """
        Get game result
        Return: (winner_player, loser_player, description)
        """
        if self.choice1 == self.choice2:
            return (None, None, "TIE")
        
        # Rock beats Scissors
        if self.choice1 == Choice.ROCK and self.choice2 == Choice.SCISSORS:
            return (self.player1, self.player2, f"{self.choice1.value} > {self.choice2.value}")
        
        # Paper beats Rock
        if self.choice1 == Choice.PAPER and self.choice2 == Choice.ROCK:
            return (self.player1, self.player2, f"{self.choice1.value} > {self.choice2.value}")
        
        # Scissors beats Paper
        if self.choice1 == Choice.SCISSORS and self.choice2 == Choice.PAPER:
            return (self.player1, self.player2, f"{self.choice1.value} > {self.choice2.value}")
        
        # Reverse
        if self.choice2 == Choice.ROCK and self.choice1 == Choice.SCISSORS:
            return (self.player2, self.player1, f"{self.choice2.value} > {self.choice1.value}")
        
        if self.choice2 == Choice.PAPER and self.choice1 == Choice.ROCK:
            return (self.player2, self.player1, f"{self.choice2.value} > {self.choice1.value}")
        
        if self.choice2 == Choice.SCISSORS and self.choice1 == Choice.PAPER:
            return (self.player2, self.player1, f"{self.choice2.value} > {self.choice1.value}")

class ChannelRPSView(discord.ui.View):
    """Shared in-channel view with buttons for both players.

    Buttons are visible in the channel. When a player clicks a button their
    choice is recorded and they receive an ephemeral confirmation. Choices
    remain hidden until both players have chosen or timeout occurs.
    """

    def __init__(self, game: RPSGame, players: Dict[int, discord.Member], timeout: int = 30):
        super().__init__(timeout=timeout)
        self.game = game
        self.players = players  # mapping of player_id -> Member

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Allow only the two players to interact with the buttons
        if interaction.user.id in self.players:
            return True
        await interaction.response.send_message("❌ You are not a player in this game!", ephemeral=True)
        return False

    async def record_choice(self, interaction: discord.Interaction, choice: Choice):
        user = interaction.user
        if (user.id == self.game.player1.id and self.game.choice1 is not None) or \
           (user.id == self.game.player2.id and self.game.choice2 is not None):
            await interaction.response.send_message("⚠️ You already chose and cannot change!", ephemeral=True)
            return

        self.game.set_choice(user, choice)
        await interaction.response.send_message(f"✅ Choice recorded: {choice.value}", ephemeral=True)

        # If both have chosen, stop the view so the caller can proceed
        if self.game.is_complete():
            self.stop()

    @discord.ui.button(label="✊ Rock", style=discord.ButtonStyle.primary)
    async def rock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.record_choice(interaction, Choice.ROCK)

    @discord.ui.button(label="📄 Paper", style=discord.ButtonStyle.success)
    async def paper_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.record_choice(interaction, Choice.PAPER)

    @discord.ui.button(label="✂️ Scissors", style=discord.ButtonStyle.danger)
    async def scissors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.record_choice(interaction, Choice.SCISSORS)


class RPSBotView(discord.ui.View):
    """Single-player view for choosing vs the bot."""

    def __init__(self, author: discord.Member, timeout: int = 30):
        super().__init__(timeout=timeout)
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ You are not the player in this game!", ephemeral=True)
            return False
        return True

    async def finish_game(self, interaction: discord.Interaction, player_choice: Choice):
        bot_choice = random.choice(list(Choice))

        # determine outcome
        if player_choice == bot_choice:
            result = 'tie'
        else:
            if (player_choice == Choice.ROCK and bot_choice == Choice.SCISSORS) or \
               (player_choice == Choice.PAPER and bot_choice == Choice.ROCK) or \
               (player_choice == Choice.SCISSORS and bot_choice == Choice.PAPER):
                result = 'win'
            else:
                result = 'lose'

        embed = discord.Embed(
            title="🎮 RPS vs Bot",
            color=discord.Color.green() if result == 'win' else discord.Color.red() if result == 'lose' else discord.Color.gold()
        )
        embed.add_field(name=f"👤 {self.author.name}", value=player_choice.value, inline=True)
        embed.add_field(name="🤖 Bot", value=bot_choice.value, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)

        if result == 'win':
            embed.add_field(name="🎉 Result", value=f"**{self.author.mention} wins!**", inline=False)
        elif result == 'lose':
            embed.add_field(name="😢 Result", value=f"**Bot wins! {self.author.mention} loses.**", inline=False)
        else:
            embed.add_field(name="🤝 Result", value="**It's a tie!**", inline=False)

        # disable buttons
        for child in self.children:
            child.disabled = True

        try:
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception:
            # fallback: send new message if edit fails
            await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="✊ Rock", style=discord.ButtonStyle.primary)
    async def rock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.finish_game(interaction, Choice.ROCK)

    @discord.ui.button(label="📄 Paper", style=discord.ButtonStyle.success)
    async def paper_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.finish_game(interaction, Choice.PAPER)

    @discord.ui.button(label="✂️ Scissors", style=discord.ButtonStyle.danger)
    async def scissors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.finish_game(interaction, Choice.SCISSORS)

class RockPaperScissors(commands.Cog):
    """Cog for Rock Paper Scissors Multiplayer game"""
    
    def __init__(self, bot):
        self.bot = bot
        self.active_games: Dict[int, RPSGame] = {}  # channel_id -> RPSGame
    
    @commands.command(name='rps', help='Play Rock Paper Scissors with another player (2 players)')
    async def rock_paper_scissors(self, ctx, opponent: discord.Member):
        """
        Play Rock Paper Scissors with another player
        Usage: !rps @opponent
        """
        
        # Check opponent
        if opponent.id == ctx.author.id:
            await ctx.send("❌ You cannot play with yourself!")
            return
        
        if opponent.bot:
            await ctx.send("❌ You cannot play with a bot!")
            return
        
        # Check if there's a game already running
        if ctx.channel.id in self.active_games:
            await ctx.send("⚠️ A Rock Paper Scissors game is already running in this channel!")
            return
        
        # Create new game
        game = RPSGame(ctx.author, opponent, ctx.channel)
        self.active_games[ctx.channel.id] = game
        
        try:
            # Send start notification
            embed = discord.Embed(
                title="🎮 Rock Paper Scissors Multiplayer",
                description=f"{ctx.author.mention} challenged {opponent.mention}!",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="⏳ Time",
                value="Each player has **30 seconds** to choose",
                inline=False
            )
            embed.add_field(
                name="📝 Rules",
                value="Result shows only when both choose\n"
                      "If time runs out with only 1 choosing = lose",
                inline=False
            )
            
            # Create and send an in-channel view with buttons for both players
            players_map = {ctx.author.id: ctx.author, opponent.id: opponent}
            view = ChannelRPSView(game, players_map, timeout=30)
            game.game_message = await ctx.send(embed=embed, view=view)

            # Wait until both players choose or the view times out
            await view.wait()

            # disable buttons after completion/timeout
            for child in view.children:
                child.disabled = True
            try:
                await game.game_message.edit(view=view)
            except Exception:
                pass

            # Handle result
            await self.show_result(game, ctx.channel)
            
        finally:
            # Remove game from list
            if ctx.channel.id in self.active_games:
                del self.active_games[ctx.channel.id]
    
    async def show_result(self, game: RPSGame, channel: discord.TextChannel):
        """Show game result"""
        
        # Check who chose and who didn't
        if game.choice1 is None and game.choice2 is None:
            embed = discord.Embed(
                title="❌ Game Cancelled",
                description="Both players failed to choose within 30 seconds!",
                color=discord.Color.red()
            )
            await channel.send(embed=embed)
            return
        
        if game.choice1 is None:
            # Player 1 lost
            embed = discord.Embed(
                title="⏱️ Time's Up - Player 1 Lost!",
                color=discord.Color.red()
            )
            embed.add_field(name=f"😢 {game.player1.name}", value="Didn't choose within 30 seconds", inline=True)
            embed.add_field(name=f"🎉 {game.player2.name}", value=f"Won! ({game.choice2.value})", inline=True)
            await channel.send(embed=embed)
            return
        
        if game.choice2 is None:
            # Player 2 lost
            embed = discord.Embed(
                title="⏱️ Time's Up - Player 2 Lost!",
                color=discord.Color.red()
            )
            embed.add_field(name=f"🎉 {game.player1.name}", value=f"Won! ({game.choice1.value})", inline=True)
            embed.add_field(name=f"😢 {game.player2.name}", value="Didn't choose within 30 seconds", inline=True)
            await channel.send(embed=embed)
            return
        
        # Both chose - calculate result
        winner, loser, description = game.get_result()
        
        if winner is None:  # Tie
            embed = discord.Embed(
                title="🤝 Result: TIE!",
                color=discord.Color.gold()
            )
            embed.add_field(name=f"👤 {game.player1.name}", value=game.choice1.value, inline=True)
            embed.add_field(name=f"👤 {game.player2.name}", value=game.choice2.value, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="🤝 Result", value="**Both chose the same!**", inline=False)
        else:
            embed = discord.Embed(
                title="🎉 Result: Someone Won!",
                color=discord.Color.green()
            )
            embed.add_field(name=f"🎉 {winner.name}", value=game.choice1.value if winner.id == game.player1.id else game.choice2.value, inline=True)
            embed.add_field(name=f"😢 {loser.name}", value=game.choice1.value if loser.id == game.player1.id else game.choice2.value, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.add_field(name="⚔️ Result", value=f"**{description}**", inline=False)
            embed.add_field(name="🏆 Winner", value=f"{winner.mention}", inline=False)
        
        await channel.send(embed=embed)
    
    @commands.command(name='rpsbot', help='Play Rock Paper Scissors against the bot')
    async def rps_vs_bot(self, ctx, choice: str = None):
        """Play RPS against the bot. Usage: `!rpsbot [rock/paper/scissors]` or `!rpsbot [1/2/3]`"""
        choices = {
            '1': Choice.ROCK,
            '2': Choice.PAPER,
            '3': Choice.SCISSORS,
            'rock': Choice.ROCK,
            'paper': Choice.PAPER,
            'scissors': Choice.SCISSORS,
            'r': Choice.ROCK,
            'p': Choice.PAPER,
            's': Choice.SCISSORS,
        }

        if choice is None:
            embed = discord.Embed(
                title="🎮 RPS vs Bot",
                description="Click a button below to play against the bot (your confirmation is ephemeral).",
                color=discord.Color.blue()
            )
            view = RPSBotView(ctx.author, timeout=30)
            await ctx.send(embed=embed, view=view)
            return

        choice_key = choice.lower().strip()
        if choice_key not in choices:
            await ctx.send("❌ Invalid choice. Use `!rpsbot 1` or `!rpsbot rock`")
            return

        player_choice = choices[choice_key]
        bot_choice = random.choice(list(Choice))

        # determine outcome
        if player_choice == bot_choice:
            result = 'tie'
        else:
            # player wins cases
            if (player_choice == Choice.ROCK and bot_choice == Choice.SCISSORS) or \
               (player_choice == Choice.PAPER and bot_choice == Choice.ROCK) or \
               (player_choice == Choice.SCISSORS and bot_choice == Choice.PAPER):
                result = 'win'
            else:
                result = 'lose'

        embed = discord.Embed(
            title="🎮 RPS vs Bot",
            color=discord.Color.green() if result == 'win' else discord.Color.red() if result == 'lose' else discord.Color.gold()
        )
        embed.add_field(name=f"👤 {ctx.author.name}", value=player_choice.value, inline=True)
        embed.add_field(name="🤖 Bot", value=bot_choice.value, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)

        if result == 'win':
            embed.add_field(name="🎉 Result", value=f"**{ctx.author.mention} wins!**", inline=False)
        elif result == 'lose':
            embed.add_field(name="😢 Result", value=f"**Bot wins! {ctx.author.mention} loses.**", inline=False)
        else:
            embed.add_field(name="🤝 Result", value="**It's a tie!**", inline=False)

        await ctx.send(embed=embed)
    
    @commands.command(name='rpshelp', help='Display Rock Paper Scissors Multiplayer guide')
    async def rps_help(self, ctx):
        """Display detailed guide"""
        embed = discord.Embed(
            title="📖 Rock Paper Scissors Multiplayer Guide",
            description="Rock Paper Scissors game between 2 players",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="🎮 How to Play",
            value="`!rps @opponent`",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ How It Works",
            value="1️⃣ Player types `!rps @opponent`\n"
                  "2️⃣ Use the in-channel buttons to choose\n"
                  "3️⃣ Click 🪨 📄 ✂️ button to choose (you'll get an ephemeral confirmation)\n"
                  "4️⃣ Result shows in channel when both choose or on timeout",
            inline=False
        )
        
        embed.add_field(
            name="⏳ Time",
            value="**30 seconds** to choose\n"
                  "If only 1 person chooses before timeout = they lose",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Game Rules",
            value="• ✊ Rock beats ✂️ Scissors\n"
                  "• 📄 Paper beats ✊ Rock\n"
                  "• ✂️ Scissors beats 📄 Paper\n"
                  "• Same choice = TIE",
            inline=False
        )
        
        embed.add_field(
            name="💡 Example",
            value="`!rps @John` → Play with John",
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Notes",
            value="• Choices made using in-channel buttons (confirmations are ephemeral)\n"
                  "• Cannot play with bots\n"
                  "• Cannot play with yourself",
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Setup cog"""
    await bot.add_cog(RockPaperScissors(bot))
