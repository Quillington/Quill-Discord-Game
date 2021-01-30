import discord
import configparser
import random
import json

from fruit import*
from userFruit import UserFruit

config = configparser.ConfigParser()
config.read('config.ini')

client = discord.Client()


lootTableEntries = [
    LootTable(50, [Fruit("🍎", "apple", [1, 3, 18]), Fruit("🍐", "pear", [1, 3, 18])]),
    LootTable(35, [Fruit("🍌", "banana", [2, 6, 30]), Fruit("🍓", "strawberry", [2, 6, 30])]),
    LootTable(10, [Fruit("🍇", "grapes", [3, 9, 45]), Fruit("🍊", "tangerine", [3, 9, 45])]),
    LootTable(1, [Fruit("🍏", "green apple", [4, 12, 60])])
]

users = {}

tiers = {}

class UserInfo:

    def __init__ (self):
        self.fruits = []
        self.pickedFruits = []
        self.fruitLimit = 7
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
    #noRoll indicates if the shop is merely opened
    if (not user.fruits == []) and (noRoll):
        return  True
    
    #Rolling code
    else:    
        if not user.firstMessage:
            user.remove_currency(2)
        user.firstMessage = False
        if user.check_currency(10):
            user.fruits = []
            weightList = []
            for i in lootTableEntries:
                weightList.append(i.weight)
            for _ in range(4):
                lootChoice = random.choices(lootTableEntries, weights = weightList)
                fruitChoice = random.choice(lootChoice[0].fruit)
                user.fruits += fruitChoice.emoji
            return True
        else:
            return False

def reaction_to_object(user, reaction):
    for f in lootTableEntries:
        for e in f.fruit:
            if e.emoji == reaction:
                return e

def pick_fruits(user, reaction):
    #Picks fruit if there is room in storage

    #run check if emoji is valid
    #run combine check 
    #run limit check
    #appends fruit using class
    #returns true or false

    for f in user.fruits:
        if reaction.emoji == f:
            
            if not combine_check(user, reaction_to_object(user, reaction.emoji)):
                if len(user.pickedFruits) >= user.fruitLimit:
                    return False
                user.pickedFruits.append(UserFruit(reaction_to_object(user, reaction.emoji), "⭐"))
            user.fruits.remove(reaction.emoji)
            fruitObject = reaction_to_object(user, reaction.emoji)
            user.remove_currency(fruitObject.cost[0])
            return True

def combine_check (user, newFruit):
    if not len(user.pickedFruits) == 0:
        oneCounter = 0
        twoCounter = 0
        for n in user.pickedFruits: 
            if n.star == "⭐" and newFruit == n.fruit:
                oneCounter += 1
            if n.star == "⭐⭐" and newFruit == n.fruit:
                twoCounter += 1
        if oneCounter == 2 and twoCounter == 2:
            user.pickedFruits.remove(UserFruit(newFruit, "⭐"))
            user.pickedFruits.remove(UserFruit(newFruit, "⭐"))
            user.pickedFruits.remove(UserFruit(newFruit, "⭐⭐"))
            user.pickedFruits.remove(UserFruit(newFruit, "⭐⭐"))
            
            user.pickedFruits.append(UserFruit(newFruit, "⭐⭐⭐"))
            return True
        elif oneCounter == 2:
            user.pickedFruits.remove(UserFruit(newFruit, "⭐"))
            user.pickedFruits.remove(UserFruit(newFruit, "⭐"))
            
            user.pickedFruits.append(UserFruit(newFruit, "⭐⭐"))
            return True
    return False

def split_and_sell (user, message):
    #split
    message = message.strip("$s")
    tempList = message.split(",")
    messageList = []
    for i in tempList:
        i.strip()
        i = int(i)
        messageList.append(i-1)

    #and sell
    objectList = []
    for j in messageList:
        if j <= user.fruitLimit:
            objectList.append(user.pickedFruits[j])
    
    for x in objectList:
        user.add_currency(x.fruit.cost[len(x.star)-1])
        user.pickedFruits.remove(x)
        

            
                
                  

#Message Commands:
async def send_roll(user, message, checkMessage):
    #Sends info from roll_fruits to ...
    fruitList = "".join(user.fruits)
    #.. on_message
    if checkMessage:
        message = await message.channel.send(fruitList)
        user.lastMessage = message.id
    #.. on_reaction_add
    else:
        await message.edit(content = fruitList)

    #then clears and readds appropriate reactions
    await message.clear_reactions()
        
    for f in user.fruits:
        await message.add_reaction(f)
    await message.add_reaction("🔁")


def profile_embed(user, message):
    profile = discord.Embed(title = f"{user.currency}🪙", description= "-----------------", color = 0xED9B85)    

    fValue = ""
    for f in range(user.fruitLimit):
        if f < len(user.pickedFruits):
            fValue += f" {f + 1}. {user.pickedFruits[f].fruit.emoji} {user.pickedFruits[f].star} \n"
        else:
            fValue += f" {f + 1}. \n"
        
    profile.add_field(name = "Fruit", value= fValue)
    return profile
    
                
#Events:
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    user = UserInfo.get_user(message.author.id)
    #Pulls up shop
    if message.content.startswith("$fruit"):
        if roll_fruits(user, True):
            await send_roll(user, message, True)
        else:
            await message.reply("You can't afford to roll fruit.")


    if message.content.startswith("$p"):
        
        await message.channel.send(embed = profile_embed(user, message))

    if message.content.startswith("$s"):
        split_and_sell(user, message.content)


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