import discord
import configparser
import random
import json

config = configparser.ConfigParser()
config.read('config.ini')

client = discord.Client()

fruits = {
    "apple" : "🍎", 
    "pear" : "🍐", 
    "banana" : "🍌", 
    "kiwi" : "🥝",
    "strawberry" : "🍓",
    "grapes" : "🍇",
    "tangerine" : "🍊"
}

users = {}

class UserInfo:

    def __init__ (self):
        self.fruits = []
        self.currency = 50
        self.lastMessage = 0
        self.firstMessage = True

    def check_currency(self, num):
        #pass to rolling functions before rolls
        if self.currency >= num:
            return True
        else:
            return False
        
    def remove_currency(self, num):
        self.currency -= num

    def add_currency(self, num):
        self.currency += num

    @staticmethod
    def get_user (id):
        if not (id in users):
            users.update({id : UserInfo()})
        return users[id] 

#fruitCommands:

def roll_fruits(user, noRoll):
    #add random fruits to a list and returns
    if (not user.fruits == []) and (noRoll):
        return  True
    
    else:    
        if not user.firstMessage:
            pass
            #user.remove_currency(10)
        if user.check_currency(10):
            fruitRolls = ""
            user.fruits = []
            i = 4
            while i > 0:
                fruitRolls = random.choice(list(fruits.values()))
                user.fruits.append(fruitRolls)
                i -= 1
            return True
        else:
            return False

#Message Commands:
async def send_roll(user, message, checkMessage):
    fruitList = "".join(user.fruits)
    if checkMessage:
        message = await message.channel.send(fruitList)
        user.lastMessage = message.id
    else:
        await message.edit(content = fruitList)

    await message.clear_reactions()
        
    for f in user.fruits:
        await message.add_reaction(f)
    await message.add_reaction("🔁")
    
                

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):
    user = UserInfo.get_user(message.author.id)

    if message.content.startswith('$fruit'):
        if roll_fruits(user, True):
            await send_roll(user, message, True)
        else:
            await message.reply("You can't afford to roll fruit.")

@client.event
async def on_reaction_add(reaction, author):
    user = UserInfo.get_user(author.id)
    if user.lastMessage == reaction.message.id and reaction.emoji == "🔁":
        if roll_fruits(user, False):
            await send_roll(user, reaction.message, False)
        else:
            await reaction.message.channel.send("You can't afford to roll fruit.")





client.run(config['DEFAULT']['token'])