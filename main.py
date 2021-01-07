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

userFruitDictionary = {

}

fruitCounters = {
    
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
        if not (message.author.id in userFruitDictionary):
            userFruitDictionary.update({message.author.id : []})
        userFruitDictionary[message.author.id].append(fruitChoice)
        reply = await message.channel.send(fruitChoice)
        await reply.add_reaction(fruits[fruitChoice])


    if message.content.startswith('$total'): 
        for fruit in list(fruits.keys()):
            fruitCounters.update({fruit : 0})
        reply2 = ""
        for item in userFruitDictionary[message.author.id]:
            fruitCounters[item] += 1
        for k in fruitCounters:
            reply2 = reply2 + f", {fruitCounters[k]} {k}"
        
        await message.channel.send(f"During this session{reply2} have been rolled.")

client.run(config['DEFAULT']['token'])