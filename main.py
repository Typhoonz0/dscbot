import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='--', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
"""
@bot.command()
async def help(ctx):
    help_text = 
    **Help Menu**
    `--help` - Display this help menu.
    `--kick @user [reason]` - Kick a user from the server.
    `--mute @user [reason]` - Mute a user in the server.
    `--timeout @user duration [reason]` - Timeout a user for a specific duration (in seconds).
    `--nickname @user new_nickname` - Change the nickname of a user.
    `--quote` - Reply to a message with this to add it to quotes.
    await ctx.send(help_text)
"""
@bot.event
async def on_message(message):
    if message.content.startswith('--quote'):
        channel = discord.utils.get(message.guild.channels, name='quotes-channel')
        if channel:
            await channel.send(f'Quote from {message.author}: {message.content[7:].strip()}')
    await bot.process_commands(message)

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked. Reason: {reason}')

@bot.command()
@has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if not muted_role:
        muted_role = await ctx.guild.create_role(name='Muted')
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f'User {member} has been muted. Reason: {reason}')

@bot.command()
@has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    await member.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=duration), reason=reason)
    await ctx.send(f'User {member} has been timed out for {duration} seconds. Reason: {reason}')

@bot.command()
@has_permissions(manage_nicknames=True)
async def nickname(ctx, member: discord.Member, *, new_nickname):
    await member.edit(nick=new_nickname)
    await ctx.send(f'User {member} nickname has been changed to {new_nickname}')

@kick.error
@mute.error
@timeout.error
@nickname.error
async def command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have the necessary permissions to use this command.")

# Replace 'your_token_here' with your bot's token
bot.run('MTI0OTg5NjU0NjMwMDk4NTQxNQ.Gumcxw.xu9xCI1gpTr7m-Tfxz2FGPkxRBIbf5OAyB8BtQ')
