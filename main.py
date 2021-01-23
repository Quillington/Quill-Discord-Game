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
        self.pickedFruits = []
        self.fruitLimit = 5
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

def pick_fruits(user, reaction):
    #Picks fruit if there is room in storage
    if len(user.pickedFruits) >= user.fruitLimit:
        return False
    for f in user.fruits:
            if reaction.emoji == f:
                user.pickedFruits.append(f)
                user.fruits.remove(f)
                return True

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

    
                
#Events:
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):
    user = UserInfo.get_user(message.author.id)
    #Pulls up shop
    if message.content.startswith('$fruit'):
        if roll_fruits(user, True):
            await send_roll(user, message, True)
        else:
            await message.reply("You can't afford to roll fruit.")

@client.event
async def on_reaction_add(reaction, author):
    user = UserInfo.get_user(author.id)
    #Edits shop message with new rolls when repeat is reacted
    if user.lastMessage == reaction.message.id and reaction.emoji == "🔁":
        if roll_fruits(user, False):
            await send_roll(user, reaction.message, False)
        else:
            await reaction.message.channel.send("You can't afford to roll fruit.")

    #Handles picking and rolling when there is only one fruit left.
    elif (user.lastMessage == reaction.message.id) and (reaction.emoji in user.fruits) and (len(user.fruits) == 1):
        if pick_fruits(user, reaction) and roll_fruits(user, False):
            await send_roll(user, reaction.message, False)
        elif not pick_fruits(user, reaction):
            await reaction.message.channel.send(f"You have too many fruits in storage ({user.fruitLimit}).")
        else:
            await reaction.message.channel.send("You can't afford to roll fruit.")

    #Normal picking and shop refresh
    elif (user.lastMessage == reaction.message.id) and (reaction.emoji in user.fruits):
        if pick_fruits(user, reaction):
            await send_roll(user, reaction.message, False)
        else:
            await reaction.message.channel.send(f"You have too many fruits in storage ({user.fruitLimit}).")

        


client.run(config['DEFAULT']['token'])