import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

my_intents = discord.Intents.default()
my_intents.messages = True
my_intents.guild_polls = True
my_intents.bans = True
my_intents.message_content = True
my_intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=my_intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
       await ctx.send("Only admin can perform this action")
    else:
        print(error)
        await ctx.send("Unknown error occurred")

@bot.command(name="hello")
async def say_hello(ctx):
    await ctx.send("Hi!")

@bot.command(name="kick")
@commands.has_role("Admin")
@commands.has_permissions(kick_members=True)
async def kick_user(ctx, member: discord.Member, reason="Because I am admin lmao"):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role in member.roles:
       await ctx.send("You cannot kick an admin")
       return

    await member.kick(reason=reason)
    await ctx.send(f"{member.name} has been kicked from the server")

@bot.command(name="vc_move")
@commands.has_role("Admin")
async def move_user(ctx, member:discord.Member, channel_name: str):
    channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
    if channel is None:
        await ctx.send(f"{channel_name} channel does not exist")
        return

    if member.voice is None:
        await ctx.send(f"{member.name} is not in a voice channel")
        return

    if member.voice.channel == channel:
        await ctx.send(f"{member.name} is already in the channel")
        return

    await member.move_to(channel)
    await ctx.send(f"Moved {member.name} to {channel_name}")

bot.run(TOKEN)
