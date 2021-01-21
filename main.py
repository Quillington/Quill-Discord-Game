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
    "kiwi" : "🥝"
}

users = {}

class UserInfo:

    def __init__ (self):
        self.fruits = []
        self.currency = 20

    def check_currency(self, num):
        #pass to rolling functions before rolls
        if self.currency >= num:
            return True
        else:
            return False
        
    def remove_currency(self, num):
        self.currency -= num

    @staticmethod
    def get_user (id):
        if not (id in users):
            users.update({id : UserInfo()})
        return users[id] 

#fruitCommands:
def open_shop(user):
    #opens up shop with previous rolls
    if user.fruits == []:
        roll_fruits(user)
    else:
        return user.fruits

def roll_fruits(user):
    #add random fruits to a list and returns
    fruitRolls = ""
    totalRolls = [] 
    if user.check_currency(10):
        user.remove_currency(10)
        user.fruits = []
        i = 4
        while i > 0:
            fruitRolls = random.choice(list(fruits.values()))
            user.fruits.append(fruitRolls)
            totalRolls.append(fruitRolls)
            i -= 1
        return totalRolls
    else:
        return ["You do not have enough money to roll fruit."]
    
        
        



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_message(message):
    user = UserInfo.get_user(message.author.id)

    if message.content.startswith('$fruit'): 
        
        reply = ""
        for i in roll_fruits(user):
            reply = reply + i
        await message.channel.send(reply)


    if message.content.startswith('$total'): 
        fruitCounters = {}

        for fruit in list(fruits.keys()):
            fruitCounters.update({fruit : 0})
        reply2 = ""
        for item in user.fruits:
            fruitCounters[item] += 1
        for k in fruitCounters:
            reply2 = reply2 + f", {fruitCounters[k]} {k}"
        
        await message.channel.send(f"During this session{reply2} have been rolled.")

client.run(config['DEFAULT']['token'])