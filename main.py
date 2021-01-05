import discord
import configparser
import random

config = configparser.ConfigParser()
config.read('config.ini')

client = discord.Client()

fruits = {
    "apple" : "🍎", 
    "pear" : "🍐", 
    "banana" : "🍌", 
    "kiwi" : "🥝"
}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$fruit'): 
        fruitChoice = random.choice(list(fruits.keys()))
        
        reply = await message.channel.send(fruitChoice)
        await reply.add_reaction(fruits[fruitChoice])

client.run(config['DEFAULT']['token'])