from discord.ext import commands, tasks
from calendar import monthrange
import datetime as dt
from datetime import datetime
import discord
import numpy as np
import re
import os

client = commands.Bot(command_prefix='!')
dataFile = "data.npy"


try:
    data = np.load(dataFile, allow_pickle='TRUE').item()
except:
    np.save(dataFile, {})


if not os.path.isdir("backups"):
   os.makedirs("backups")


def load(userID, roleName, guildID, amount, type):
    inty = 0
    intm = 0
    intd = 0
    inth = 0
    intM = 0

    if type == "y":
        inty = amount
    if type == "M":
        intM = amount
    if type == "d":
        intd = amount
    if type == "h":
        inth = amount
    if type == "m":
        intm = amount

    data = np.load(dataFile, allow_pickle='TRUE').item()
    now = datetime.now()

    while int(now.strftime("%M")) + intm >= 60:
        intm -= 60
        inth += 1

    while int(now.strftime("%H")) + inth >= 24:
        inth -= 24
        intd += 1

    if int(now.strftime("%m")) + intM < 12:
        while int(now.strftime("%d")) + intd > monthrange(int(now.strftime("%Y")), int(now.strftime("%m")) + intM)[1]:
            intd -= monthrange(int(now.strftime("%Y")), int(now.strftime("%m")) + intM)[1]
            intM += 1
            while int(now.strftime("%m")) + intM > 12:
                intM -= 12
                inty += 1

    while int(now.strftime("%m")) + intM > 12:
        intM -= 12
        inty += 1

    time = [int(now.strftime("%Y")) + inty, int(now.strftime("%m")) + intM, int(now.strftime("%d")) + intd,
            int(now.strftime("%H")) + inth, int(now.strftime("%M")) + intm]
    data[len(data) + 1] = [time, userID, str(roleName), guildID]
    np.save(dataFile, data)


@client.command('removerole')
@commands.has_permissions(manage_roles=True)
async def role(ctx, user : discord.Member, *, role : discord.Role):
    if role.position > ctx.author.top_role.position:
        return await ctx.send(f"")

    if ctx.author.top_role <= user.top_role:
        return await ctx.send("You can not change role of an user with the same or higher role")

    if role not in user.roles:
        return await ctx.send(f"User **{user}** (`{user.id}`) does not have role **{role}** (`{role.id}`)")

    if role in user.roles:
        await user.remove_roles(role)
        await user.send(f"Role **{role}** na server **{ctx.guild}** has been taken from you")
        await ctx.send(f"Role **{role}** (`{role.id}`) has been taken from user **{user}** (`{user.id}`) 👌")
        data = np.load(dataFile, allow_pickle='TRUE').item()
        for x in data:
            if data.get(x)[1] == user.id:
                data.pop(x)
                np.save(dataFile, data)
                return


@client.command('addrole')
@commands.has_permissions(manage_roles=True)
async def role(ctx, user : discord.Member, role : discord.Role, *, days: str):

    try:
        match = re.match(r"([0-9]+)([a-z]+)", days, re.I)
        items = match.groups()
    except:
        return await ctx.send(f"**{days}** is not a acceptable value")

    if ctx.author.top_role <= user.top_role:
        return await ctx.send("You can not change role of an user with the same or higher role")

    if role.position >= ctx.author.top_role.position:
        return await ctx.send('You can not give higher or equal role as your own')

    if role in user.roles:
        return await ctx.send(f"**{user}** (`{user.id}`) already has role **{role}** (`{role.id}`)")

    if items[1] == "m":
        if items[0] == "1":
            name = "minute"
        else:
            name = "minutes"
    elif items[1] == "h":
        if items[0] == "1":
            name = "hour"
        else:
            name = "hours"
    elif items[1] == "d":
        if items[0] == "1":
            name = "day"
        else:
            name = "days"
    elif items[1] == "M":
        if items[0] == "1":
            name = "month"
        else:
            name = "months"
    elif items[1] == "y":
        if items[0] == "1":
            name = "year"
        else:
            name = "years"
    else:
        return await ctx.send(f"**{items[1]}** is not a acceptable value")

    await user.add_roles(role)
    id = ctx.message.guild.id
    load(user.id, role, id, int(items[0]), items[1])
    await ctx.send(f"You gave role **{role}** (`{role.id}`) to user **{user}** (`{user.id}`) 👌")
    await user.send(f"You got role **{role}** on server **{role.guild}** for **{items[0]} {name}**")


def reload(data):
    lenght = len(data)
    number = 0
    value = 0
    newData = {}
    while number != lenght:
        h = data.get(value)
        if h != None:
            newData[number] = h
            number += 1
        value += 1
    return newData


@tasks.loop(hours=24)
async def backups():
    data = np.load(dataFile, allow_pickle='TRUE').item()
    if data != {}:
        now = datetime.now()
        np.save("backups/" + str(dt.date.today()) + "-" + now.strftime("%H") + "." + now.strftime("%M") + ".npy", data)


@tasks.loop(minutes=1)
async def f():
    await client.wait_until_ready()

    def check(data, x):
        if data.get(x)[0][0] < int(datetime.now().strftime("%Y")):
            return True

        elif data.get(x)[0][0] > int(datetime.now().strftime("%Y")):
            return False

        if data.get(x)[0][1] < int(datetime.now().strftime("%m")):
            return True

        elif data.get(x)[0][1] > int(datetime.now().strftime("%m")):
            return False

        if data.get(x)[0][2] < int(datetime.now().strftime("%d")):
            return True

        elif data.get(x)[0][2] > int(datetime.now().strftime("%d")):
            return False

        if data.get(x)[0][3] < int(datetime.now().strftime("%H")):
            return True

        elif data.get(x)[0][3] > int(datetime.now().strftime("%H")):
            return False

        if data.get(x)[0][4] <= int(datetime.now().strftime("%M")):
            return True

    data = np.load(dataFile, allow_pickle='TRUE').item()
    topop = []
    done = False
    for x in data:
        try:
            if check(data, x):
                guild = client.get_guild(data[x][3])
                user = await guild.fetch_member(int(data[x][1]))
                rolee = data.get(x)[2]
                role = discord.utils.get(guild.roles, name=rolee)
                await user.send(f"Your role **{rolee}** on server **{guild}** has expired")
                await user.remove_roles(role)
                topop.append(x)
                done = True
        except:
            break

    if done:
        for x in topop:
            data.pop(x)
        data = reload(data)
        np.save(dataFile, data)

backups.start()
f.start()
client.run('OTk0OTU0MzE0NzMwNzEzMjA5.GDJ-Hr._oKikw6uiHizFUwGh44_0dMkttUcjVj5PI2JlA')
