"""
Cog Example - Fun Commands
"""
import discord
from discord.ext import commands
import random

class ChooseModal(discord.ui.Modal, title="Choose from Options"):
    """Modal for entering up to 5 options to choose from."""
    
    option1 = discord.ui.TextInput(label="Option 1", placeholder="Enter first option", required=True)
    option2 = discord.ui.TextInput(label="Option 2", placeholder="Enter second option", required=True)
    option3 = discord.ui.TextInput(label="Option 3", placeholder="Enter third option", required=False)
    option4 = discord.ui.TextInput(label="Option 4", placeholder="Enter fourth option", required=False)
    option5 = discord.ui.TextInput(label="Option 5", placeholder="Enter fifth option", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        # Collect non-empty options
        options = [
            self.option1.value,
            self.option2.value,
        ]
        if self.option3.value:
            options.append(self.option3.value)
        if self.option4.value:
            options.append(self.option4.value)
        if self.option5.value:
            options.append(self.option5.value)
        
        chosen = random.choice(options)
        
        embed = discord.Embed(
            title="🎯 Random Choice",
            description=f"{interaction.user.mention}, I choose:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Options", value="\n".join(f"• {opt}" for opt in options), inline=False)
        embed.add_field(name="✨ Result", value=f"**{chosen}**", inline=False)
        
        await interaction.response.send_message(embed=embed)

class DiceRollView(discord.ui.View):
    """View for selecting number of dice to roll."""

    def __init__(self, author: discord.Member, timeout: int = 30):
        super().__init__(timeout=timeout)
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ You are not the player in this game!", ephemeral=True)
            return False
        return True

    async def roll_and_show(self, interaction: discord.Interaction, num_dice: int):
        results = [random.randint(1, 6) for _ in range(num_dice)]
        total = sum(results)

        # Build result string
        result_str = " + ".join(str(r) for r in results)
        
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"{self.author.mention} rolled **{num_dice}** dice",
            color=discord.Color.blue()
        )
        embed.add_field(name="Results", value=result_str, inline=False)
        embed.add_field(name="Total", value=f"**{total}**", inline=False)

        # disable buttons
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="1 Dice", style=discord.ButtonStyle.primary)
    async def roll_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.roll_and_show(interaction, 1)

    @discord.ui.button(label="2 Dice", style=discord.ButtonStyle.primary)
    async def roll_two(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.roll_and_show(interaction, 2)

    @discord.ui.button(label="3 Dice", style=discord.ButtonStyle.primary)
    async def roll_three(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.roll_and_show(interaction, 3)

class Fun(commands.Cog):
    """Fun commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='dice', aliases=['d'], help='Roll a dice')
    async def roll_dice(self, ctx):
        """Roll a 6-sided dice"""
        result = random.randint(1, 6)
        await ctx.send(f'🎲 {ctx.author.mention} rolled: **{result}**')
    
    @commands.command(name='diceroll', aliases=['dr'], help='Roll 1, 2, or 3 dice with button interface')
    async def dice_roll(self, ctx):
        """Roll dice with button interface to select 1, 2, or 3 dice"""
        embed = discord.Embed(
            title="🎲 Dice Roller",
            description="Click a button below to roll dice",
            color=discord.Color.blue()
        )
        view = DiceRollView(ctx.author, timeout=30)
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name='coin', help='Flip a coin')
    async def flip_coin(self, ctx):
        """Flip a coin"""
        result = random.choice(['Heads', 'Tails'])
        emoji = '🪙'
        await ctx.send(f'{emoji} {ctx.author.mention}: **{result}**')

    @commands.command(name='cf', aliases=['coinflip'], help='Flip a coin (alias: coinflip)')
    async def coinflip(self, ctx):
        """Flip a coin using the `!cf` shortcut or `!coinflip`."""
        result = random.choice(['Heads', 'Tails'])
        emoji = '🪙'
        await ctx.send(f'{emoji} {ctx.author.mention}: **{result}**')
    
    @commands.command(name='random', aliases=['r', 'rand'], help='Pick a random number')
    async def random_number(self, ctx, min_num: int, max_num: int):
        """Pick a random number between min_num and max_num"""
        if min_num > max_num:
            await ctx.send('❌ Minimum number must be less than or equal to maximum number!')
            return
        
        result = random.randint(min_num, max_num)
        await ctx.send(f'🎯 Random number between {min_num} and {max_num}: **{result}**')
    
    @commands.command(name='choose', aliases=['ch', 'pick'], help='Choose a random option')
    async def choose_option(self, ctx):
        """Choose a random option from a list (up to 5 options via modal)"""
        modal = ChooseModal()
        await ctx.interaction.response.send_modal(modal) if hasattr(ctx, 'interaction') else await ctx.send("Please use this command in a server where it can respond with a modal.")
        
        # Alternative: send modal via button
        embed = discord.Embed(
            title="🎯 Choose a Random Option",
            description="Click the button to enter up to 5 options",
            color=discord.Color.blue()
        )
        
        view = discord.ui.View()
        
        async def show_modal(interaction: discord.Interaction):
            await interaction.response.send_modal(ChooseModal())
        
        button = discord.ui.Button(label="Enter Options", style=discord.ButtonStyle.primary)
        button.callback = show_modal
        view.add_item(button)
        
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    """Setup cog"""
    await bot.add_cog(Fun(bot))
