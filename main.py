import discord
import asyncio
import configparser
import random
import json
import sqlite3

from operator import itemgetter, attrgetter

config = configparser.ConfigParser()
config.read('config.ini')

client = discord.Client()


conn = sqlite3.connect('sqlTables.db')
c = conn.cursor()
conn.row_factory = sqlite3.Row
#database that stores all user data related to mostly money and global user stuff
c.execute('''CREATE TABLE userTable
    (id TEXT NOT NULL PRIMARY KEY, currency INT, lastMessage TEXT, firstMessage BOOL)''')
#database that stores what the main card is.
c.execute('''CREATE TABLE userCard
    (id TEXT NOT NULL PRIMARY KEY, name TEXT, titleShort TEXT, index TINYINT)''')
#database that stores all cards and their gear
c.execute('''CREATE TABLE cards
    (id TEXT, name TEXT, titleShort TEXT, index TINYINT, gearNameOne, gearNameTwo, gearNameThree, gearNameFour)''')
c.execute('CREATE INDEX useridcards ON cards (id)')


#on message event
#send $f or $farm for gaining currency. Based on GS of current main card








client.run(config['DEFAULT']['token'])