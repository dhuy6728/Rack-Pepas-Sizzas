"""
Cog - Moderation Commands
"""
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    """Moderation commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='kick', help='Kick a member from server')
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, member: discord.Member, *, reason='No reason provided'):
        """Kick a member"""
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title='🚪 Member Kicked',
                color=discord.Color.red()
            )
            embed.add_field(name='Member', value=member.mention, inline=False)
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.add_field(name='Kicked by', value=ctx.author.mention, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'❌ Error: {e}')
    
    @commands.command(name='ban', help='Ban a member from server')
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, member: discord.Member, *, reason='No reason provided'):
        """Ban a member"""
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title='🚫 Member Banned',
                color=discord.Color.dark_red()
            )
            embed.add_field(name='Member', value=member.mention, inline=False)
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.add_field(name='Banned by', value=ctx.author.mention, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'❌ Error: {e}')
    
    @commands.command(name='mute', help='Mute a member')
    @commands.has_permissions(manage_messages=True)
    async def mute_member(self, ctx, member: discord.Member):
        """Mute a member"""
        try:
            await member.edit(reason='Muted')
            await ctx.send(f'🔇 {member.mention} has been muted')
        except Exception as e:
            await ctx.send(f'❌ Error: {e}')
    
    @commands.command(name='clear', help='Delete messages')
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int):
        """Delete number of messages"""
        if amount <= 0:
            await ctx.send('❌ Message amount must be greater than 0!')
            return
        
        if amount > 100:
            await ctx.send('❌ Can only delete up to 100 messages!')
            return
        
        try:
            deleted = await ctx.channel.purge(limit=amount)
            await ctx.send(f'🗑️ Deleted {len(deleted)} messages!')
        except Exception as e:
            await ctx.send(f'❌ Error: {e}')

async def setup(bot):
    """Setup cog"""
    await bot.add_cog(Moderation(bot))
