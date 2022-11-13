import discord
import random
import datetime
import aiosqlite


from discord.ext import commands
import os

client = commands.Bot(command_prefix = "!", help_command=None)

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def coinflip(ctx):
    number = random.randint(1,2)

    if number == 1:
        await ctx.send("Heads!")
    if number == 2:
        await ctx.send("Tails!")

@client.command()
async def rps(ctx, hand):
    hand = hand.lower()
    hands = ["rock", "paper", "scissors"]

    bothand = random.choice(hands)
    await ctx.send(bothand)

    if hand == bothand:
        await ctx.send("Draw!")

    if hand == "paper":
        if bothand == "rock":
            await ctx.send("You won!")
        if bothand == "scissors":
            await ctx.send("I won!")
    elif hand == "rock":
        if bothand == "scissors":
            await ctx.send("You won!")
        if bothand == "paper":
            await ctx.send("I won!")
    elif hand == "scissors":
        if bothand == "paper":
            await ctx.send("You won!")
        if bothand == "rock":
            await ctx.send("I won!")

@client.command(aliases = ["about"])
async def help(ctx):
    MyEmbed = discord.Embed(title = "Commands", description = "These are the Commands that you can use for this bot", color = discord.Color.purple())
    #MyEmbed.set_thumbnail(url = )
    MyEmbed.add_field(name = "!ping", value = "This Command replies back with Pong!", inline=False)
    MyEmbed.add_field(name="!coinflip", value="This Command flips a coin", inline=False)
    MyEmbed.add_field(name="!rps", value="This Command allows you to play rock paper scissors", inline=False)
    await ctx.send(embed = MyEmbed)

@client.group()
async def edit(ctx):
    pass

@edit.command()
async def servername(ctx,*, input):
   await ctx.guild.edit(name = input)

@edit.command()
async def region(ctx,*, input):
   await ctx.guild.edit(region = input)

@edit.command()
async def createtextchannel(ctx,*, input):
   await ctx.guild.create_text_channel(name = input)

@edit.command()
async def createvoicechannel(ctx,*, input):
   await ctx.guild.create_voice_channel(name = input)

@edit.command()
async def createrole(ctx,*, input):
   await ctx.guild.create_role(name = input)


@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    await ctx.guild.kick(member, reason = reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await ctx.guild.ban(member, reason = reason)

@client.command()
async def unban(ctx,*,input):
    name, discriminator=input.split("#")
    banned_members = await ctx.guild.bans()
    for bannedmember in banned_members:
        username = bannedmember.user.name
        disc = bannedmember.user.discriminator
        if name == username and disc == discriminator:
            await ctx.guild.unban(bannedmember.user)

@client.command()
async def clearmessage(ctx, amount ,day : int = None, month : int = None, year : int = datetime.datetime.now().year):
    if amount == " ":
        if day == None or month == None:
            return
        else:
            await ctx.channel.purge(after = datetime.datetime(day = day, month= month, year = year))
    await ctx.channel.purge(limit = int(amount)+1)

@client.command()
async def mute(ctx, member : discord.Member):
    await member.edit(mute = True)

@client.command()
async def unmute(ctx, member : discord.Member):
    await member.edit(mute = False)

@client.command()
async def deafen(ctx, member : discord.Member):
    await member.edit(deafen = True)

@client.command()
async def undeafen(ctx, member : discord.Member):
    await member.edit(deafen = False)

@client.command()
async def voicekick(ctx, member : discord.Member):
    await member.edit(voice_channel = None)

client.run(os.getenv('TOKEN'))