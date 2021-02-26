import sqlite3

from Cards import *
from Gear import *
from Powers import *


users = {}

class UserInfo:

    def __init__ (self, id):
        self.id = id
        self.currency = 50
        self.lastMessage = 0
        self.firstMessage = True
        self.cards = []
        self.mainCard = None
        #Should be an empty object until filled with a usercard object

    def check_currency(self, num):
        #pass to rolling functions before rolls
        if self.currency >= num:
            return True
        else:
            return False
        
    def remove_currency(self, num):
        self.currency -= num

    def add_currency(self):
        pass
        #add currency based on GS of card

    def sql_retrieve(self):
        conn = sqlite3.connect('sqlTables.db')
        c = conn.cursor()
        conn.row_factory = sqlite3.Row

        c = conn.cursor()
        self.id = str(self.id)
        #user table
        c.execute('SELECT * FROM userTable WHERE id = ?', (id,))  
        row = c.fetchone()
        if not (row == None):
            pass
            self.currency = row['currency']
            self.lastMessage = row['lastMessage']
            self.firstMessage = row['firstMessage']
             
        #Need to do lookups where database checks other classes to fill in missing info.
        #c.execute('SELECT * FROM fruits WHERE id = ?', (id,))
        #for row in c:
        #    user.fruits.append(row['fruit'])
       
    def get_user (self):
        if not (self.id in users):
            user = UserInfo(id)
            self.sql_retrieve()
            users.update({id : user})
        return users[id] 



class UserCard:

    def __init__ (self, card, activeSpec):
        self.card = card
        #should be the card object associated with this userCard
        self.activeSpec = activeSpec
        #default is 0 but can be changed. This number changes the index value of literally everything else in this class
        self.specCount = len (card.spec)
        self.gear = []
        for _ in range(self.specCount):
            self.gear.append([None, None, None, None])
            #these should be empty gear objects too somehow fuck
        self.GS = []
        for _ in range(self.specCount):
            self.GS.append([0])
        #All these for loops are to seperate specs and set up the nice array format

        #Constants here to not make weird array bullshit
        GEARSLOTCOUNT = 4
        NECK = 0
        RING = 1
        TRINKET = 2
        MAINHAND = 3
        #Most formulas go here
        #GS is calculated by adding the gear object GS and dividing by 4 (amount of gear slots).
        
    def addGear (self, user, gear):
        if (gear.GS > self.GS[self.activeSpec]) or not (gear.spec == self.card.spec):
            return False
        if gear.piece == "Neck":
            self.gear[self.activeSpec][NECK].append(gear)
        elif gear.piece == "Ring":
            self.gear[self.activeSpec][RING].append(gear)
        elif gear.piece == "Trinket":
            self.gear[self.activeSpec][TRINKET].append(gear)
        elif gear.piece == "Mainhand":
            self.gear[self.activeSpec][MAINHAND].append(gear)

        
    
    def updateGearScore (self):
        gearSum = 0
        for i in self.gear[self.activeSpec].GS:
            gearsum += i
        gearScore = gearSum / 4
        self.GS[self.activeSpec] = gearScore
    
    def bonusCurrency (self):
        pass

