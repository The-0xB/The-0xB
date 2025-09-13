import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# تابعني بالرسالة القادمة لأكمل الكود
