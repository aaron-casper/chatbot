#discord bot (known to work with py3.8)
from chattymarkov import ChattyMarkov
import random
markov = ChattyMarkov("json://./brain.json")
# This example requires the 'message_content' intent.
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print("---------\n")

    if message.author == client.user:
        return
    if client.user in message.mentions:
        response = "<@"+str(message.author.id)+"> " + str(markov.generate())
    if client.user not in message.mentions:
        markov.learn(message.content)
        print("learned: " + message.content)
        print("---------\n")
        response = markov.generate()

    await message.channel.send(response)
    print(str(message.author.display_name) + "|" + str(message.author.id) + "> " + str(message.content))
    print("said: " + response)
    print("---------\n")
#    if 'MrSpack' in message.mentions:

client.run('API_TOKEN')

