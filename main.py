# main.py
import discord
from discord.ext import commands
from backup_manager import BackupManager
from password_manager import PasswordManager
from lock_manager import LockManager

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-', intents=intents)

backup_manager = BackupManager(bot)
password_manager = PasswordManager()
lock_manager = LockManager(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def backup(ctx):
    if not password_manager.check_password("your_password_here"):
        await ctx.send("كلمة السر غير صحيحة.")
        return
    await backup_manager.create_backup(ctx.guild)
    await ctx.send("تم إنشاء نسخة احتياطية.")

@bot.command()
async def restore(ctx):
    if not password_manager.check_password("your_password_here"):
        await ctx.send("كلمة السر غير صحيحة.")
        return
    await backup_manager.restore_backup(ctx.guild)
    await ctx.send("تم استعادة النسخة الاحتياطية.")

@bot.command()
async def lock(ctx):
    lock_manager.add_locked_channel(str(ctx.channel.id))
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, connect=False)
    await ctx.send("تم قفل القناة.")

@bot.command()
async def unlock(ctx):
    lock_manager.remove_locked_channel(str(ctx.channel.id))
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True, connect=True)
    await ctx.send("تم فتح القناة.")

@bot.command()
async def hide(ctx):
    lock_manager.add_hidden_channel(str(ctx.channel.id))
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send("تم إخفاء القناة.")

@bot.command()
async def show(ctx):
    lock_manager.remove_hidden_channel(str(ctx.channel.id))
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send("تم إظهار القناة.")

bot.run('YOUR_BOT_TOKEN')
