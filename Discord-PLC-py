from discord.ext import commands, tasks
import snap7
from esnap7 import easyPLC
from datetime import datetime
import discord

client = commands.Bot(command_prefix='!')

pls = easyPLC.PLC()

while True:
    try:
        pls.begin('192.168.0.1', 0, 1)
    except:
        print("coudnt establish connection with PLC")
    else:
        print("connection with PLC has been established")
        break


print("enabling discord bot...")
@client.command('writePLC')
@commands.has_permissions(manage_roles=True)
async def role(ctx, tag : str, *, value: bool):
    pls.writeBoolTag("q", 0, 7, True)
    print(value, tag)

    try:
        if len(tag) != 4:
            return await ctx.send(f"**{tag}** is not an acceptable tag")
    except:
        return await ctx.send(f"**{tag}** is not an acceptable tag")

    try:
        pls.writeBoolTag(tag[0], int(tag[1]), int(tag[3]), value)
    except:
        return await ctx.send(f"you did something wrong")

    print(tag[0], int(tag[1]), int(tag[3]), value)


print("everythings seems nominal, the bot has been enabled")
client.run("Token")
