import discord
import requests
import json
import random
import os
import aiosqlite

intents = discord.Intents.all()     #this allows bot to use all intents
client = discord.Client(intents = intents)      #this allows bot to use all intents



sad_word = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']


starter_encouragements = [
    'Cheer up!',
    'Hang in there',
    'You are a great person'
]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)

    quote = json_data[0]['q'] + " - " +json_data[0]['a']

    return(quote)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}') # print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content
    username = message.author.display_name


    if message.author == client.user:
        print("answering to bot's messages blocked")
        return

    if msg.startswith('$inspire'):
        quote = get_quote()

        await message.channel.send(quote)

    if msg.startswith('$hello'):
        await message.channel.send('Hello ' + username +'!')


    #if msg.startswith('$random'):
        #gold_number = random.randint(1, 100)
        #await message.channel.send("Let's play a game! Guess the number from 1 to 100. Remember you have only 5 attempts!")

    if any(word in msg for word in sad_word):
        await message.channel.send(random.choice(starter_encouragements))


@client.event
async def on_member_join(member):
    username = member.display_name
    guild = member.guild
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"Welcome to {guildname}, {username}!")


@client.event
async def on_raw_reaction_add(payload): #Your bot can only changes less important roles
    emoji = payload.emoji.name
    member = payload.member
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = client.get_guild(guild_id)

    if emoji == "🕸️" and message_id == 984166717037105232:
        role = discord.utils.get(guild.roles, name="Professional_tester")
        await member.add_roles(role)

    if emoji == "🦇" and message_id == 984166846624305243: # 🦇
        role = discord.utils.get(guild.roles, name="Tester")
        await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    user_id = payload.user_id
    emoji = payload.emoji.name
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = client.get_guild(guild_id)
    member = guild.get_member(user_id)

    if emoji == "🕸️" and message_id == 984166717037105232:
        role = discord.utils.get(guild.roles, name="Professional_tester")
        await member.remove_roles(role)

    if emoji == "🦇" and message_id == 984166846624305243: # 🦇
        role = discord.utils.get(guild.roles, name="Tester")
        await member.remove_roles(role)



client.run(os.getenv('TOKEN'))