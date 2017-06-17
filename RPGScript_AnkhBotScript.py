#Libs
import sys
import os
import clr
clr.AddReference("IronPython.SQLite.dll")
import sqlite3
import json
import datetime
import math
import random

#Info
ScriptName = "RPGScript"
Website = ""
Creator = "Karashi"
Version = "1.0.0.0"

#Vars
g_Command = "!rpg"
g_ErrorMsg = ", the command was invalid. "

g_DirPath = os.path.dirname(os.path.abspath(__file__))
g_RPGdb = os.path.join(g_DirPath, "rpg.db")

g_TickTime = 60
g_LastTicked = datetime.datetime.now()

g_CooldownTime = 1
g_LastUsed = datetime.datetime.now()

#Init
def Init():
    #check if rpg.db exists
    if not os.path.isfile(g_RPGdb):
        #create rpg.db
        dbConnection = sqlite3.connect(g_RPGdb)
        dbCursor = dbConnection.cursor()
        #create tables
        try:
            dbCursor.execute("""CREATE TABLE chars (
                                charid INTEGER PRIMARY KEY,
                                user TEXT NOT NULL,
                                level INTEGER NOT NULL,
                                exp INTEGER NOT NULL)""")
            dbCursor.execute("""CREATE TABLE stats (
                                statid INTEGER PRIMARY KEY,
                                charid INTEGER NOT NULL,
                                points INTEGER NOT NULL,
                                str INT INTEGER NULL,
                                dex INT INTEGER NULL,
                                vit INT INTEGER NULL,
                                int INT INTEGER NULL,
                                luk INT INTEGER NULL)""")
            dbCursor.execute("""CREATE TABLE inv (
                                invid INTEGER PRIMARY KEY,
                                charid INTEGER NOT NULL,
                                money INTEGER NOT NULL,
                                items TEXT NOT NULL)""")
            dbCursor.execute("""CREATE TABLE items (
                                itemid INTEGER PRIMARY KEY,
                                item TEXT NOT NULL,
                                type TEXT NOT NULL,
                                rarity REAL NOT NULL,
                                buyprice INTEGER NOT NULL,
                                sellprice INTEGER NOT NULL)""")
            rpgItems = [("coal", "mine", 0.99, 0, 1),
                        ("copper_ore", "mine", 0.98, 0, 2),
                        ("iron_ore", "mine", 0.95, 0, 5),
                        ("silver_ore", "mine", 0.90, 0, 10),
                        ("gold_ore", "mine", 0.80, 0, 20),
                        ("mithril", "mine", 0.50, 0, 50),
                        ("adamantite", "mine", 0.25, 0, 75),
                        ("runite", "mine", 0.01, 0, 100),
                        ("oak_wood", "chop", 0.99, 0, 1),
                        ("willow_wood", "chop", 0.98, 0, 2),
                        ("maple_wood", "chop", 0.95, 0, 5),
                        ("pine_wood", "chop", 0.90, 0, 10),
                        ("yew_wood", "chop", 0.80, 0, 20),
                        ("magic_wood", "chop", 0.50, 0, 50),
                        ("elder_wood", "chop", 0.01, 0, 100),
                        ("shrimp", "fish", 0.99, 0, 1),
                        ("minnow", "fish", 0.98, 0, 2),
                        ("sardine", "fish", 0.95, 0, 5),
                        ("herring", "fish", 0.92, 0, 8),
                        ("mackerel", "fish", 0.88, 0, 12),
                        ("trout", "fish", 0.82, 0, 18),
                        ("cod", "fish", 0.76, 0, 24),
                        ("pike", "fish", 0.68, 0, 32),
                        ("salmon", "fish", 0.60, 0, 40),
                        ("tuna", "fish", 0.52, 0, 48),
                        ("swordfish", "fish", 0.40, 0, 60),
                        ("shark", "fish", 0.28, 0, 72),
                        ("whale", "fish", 0.01, 0, 100),
                        ("squirrel", "hunt", 0.99, 0, 1),
                        ("rabbit", "hunt", 0.98, 0, 2),
                        ("quail", "hunt", 0.98, 0, 2),
                        ("duck", "hunt", 0.95, 0, 5),
                        ("coyote", "hunt", 0.90, 0, 10),
                        ("deer", "hunt", 0.75, 0, 25),
                        ("moose", "hunt", 0.60, 0, 40),
                        ("boar", "hunt", 0.40, 0, 60),
                        ("bear", "hunt", 0.20, 0, 80),
                        ("bison", "hunt", 0.20, 0, 80),
                        ("potato", "farm", 0.99, 0, 1),
                        ("onion", "farm", 0.90, 0, 2),
                        ("cabbage", "farm", 0.80, 0, 5),
                        ("tomato", "farm", 0.70, 0, 5),
                        ("corn", "farm", 0.60, 0, 10),
                        ("apple", "farm", 0.50, 0, 15),
                        ("orange", "farm", 0.40, 0, 20),
                        ("strawberry", "farm", 0.30, 0, 25),
                        ("watermelon", "farm", 0.20, 0, 40),
                        ("poor_trinket", "quest", 0.95, 0, 10),
                        ("common_trinket", "quest", 0.80, 0, 20),
                        ("uncommon_trinket", "quest", 0.65, 0, 30),
                        ("rare_trinket", "quest", 0.50, 0, 40),
                        ("epic_trinket", "quest", 0.35, 0, 50),
                        ("legendary_trinket", "quest", 0.20, 0, 60),
                        ("heirloom_trinket", "quest", 0.05, 0, 70),
                        ("poor_relic", "quest", 0.90, 0, 15),
                        ("common_relic", "quest", 0.75, 0, 25),
                        ("uncommon_relic", "quest", 0.60, 0, 40),
                        ("rare_relic", "quest", 0.45, 0, 60),
                        ("epic_relic", "quest", 0.30, 0, 85),
                        ("legendary_relic", "quest", 0.15, 0, 115),
                        ("heirloom_relic", "quest", 0.01, 0, 150),
                        ("minor_potion", "shop", 0.50, 20, 10),
                        ("major_potion", "shop", 0.25, 60, 30)]
            #insert list of items into db
            dbCursor.executemany("""INSERT INTO items (
                                    \"item\", \"type\", \"rarity\", \"buyprice\", \"sellprice\")
                                    VALUES (
                                    ?, ?, ?, ?, ?)""", rpgItems)
            #commit changes and close connection
            dbConnection.commit()
            dbConnection.close()
        except sqlite3.Error as error:
            Parent.SendTwitchMessage(str(error))
            dbConnection.close()

#Execute
def Execute(data):
    if data.IsChatMessage():
        #parse message for command and args
        args = data.Message.split(" ")
        command = args[0].lower()
        #add user if not in db
        if command == g_Command:
            #connect to db
            dbConnection = sqlite3.connect(g_RPGdb)
            dbCursor = dbConnection.cursor()
            #check if user in db
            try:
                dbCursor.execute("SELECT * FROM chars WHERE user = ?", (data.User.lower(),))
                if dbCursor.fetchone() == None:
                    #initialize char info in db
                    dbCursor.execute("""INSERT INTO chars (
                                        \"user\", \"level\", \"exp\")
                                        VALUES (
                                        ?, ?, ?)""", (data.User.lower(), 1, 0))
                    dbCursor.execute("SELECT charid FROM chars WHERE user = ?", (data.User.lower(),))
                    dbCharid = dbCursor.fetchone()[0]
                    dbCursor.execute("""INSERT INTO stats (
                                        \"charid\", \"points\", \"str\", \"dex\", \"vit\", \"int\", \"luk\")
                                        VALUES (
                                        ?, ?, ?, ?, ?, ?, ?)""", (dbCharid, 0, 1, 1, 1, 1, 1))
                    dbCursor.execute("""INSERT INTO inv (
                                        \"charid\", \"money\", \"items\")
                                        VALUES (
                                        ?, ?, ?)""", (dbCharid, 0, json.dumps([])))
                    #commit changes
                    dbConnection.commit()
                #close connection
                dbConnection.close()
            except sqlite3.Error as error:
                Parent.SendTwitchMessage(str(error))
                dbConnection.close()
        #check for missing args
        if command == g_Command and len(args) < 2:
                Parent.SendTwitchMessage("{}{}\"!rpg help\" to get started.".format(data.User.lower(), g_ErrorMsg))
        elif command == g_Command and not IsOnCooldown():
            if args[1].lower() == "help":
                #display help message
                Parent.SendTwitchMessage("Available arguments for \"!rpg\" are mine, chop, fish, hunt, farm, quest, stats, assign, inv, shop.")
            elif args[1].lower() == "mine":
                #mine ore
                Parent.SendTwitchMessage("Attempting to mine some ore.")
                #connect to db
                dbConnection = sqlite3.connect(g_RPGdb)
                dbCursor = dbConnection.cursor()
                #get char info
                try:
                    dbCursor.execute("SELECT * FROM chars WHERE user = ?", (data.User.lower(),))
                    dbChar = dbCursor.fetchone()
                    dbCursor.execute("SELECT * FROM stats WHERE charid = ?", (dbChar[0],))
                    dbStats = dbCursor.fetchone()
                    dbCursor.execute("SELECT items FROM inv WHERE charid = ?", (dbChar[0],))
                    dbInv = dbCursor.fetchone()[0]
                    #parse inv
                    inv = json.loads(dbInv)
                    #get list of possible loot
                    dbCursor.execute("SELECT * FROM items WHERE type = ?", ("mine",))
                    dbItems = dbCursor.fetchall()
                    expGained = 5
                    gotLoot = False
                    #iterate through loot
                    for item in dbItems:
                        #determine loot chance
                        lootChance = (item[3] / (1.3 - random.random())) + (dbStats[3] / (100 - random.random())) + (dbStats[7] / (100 - random.random()))
                        if lootChance > 1:
                            gotLoot = True
                            #determine amount of loot
                            lootAmount = int(math.ceil((lootChance - 1) * 10) + random.randint(0, 10))
                            expGained += 5 * lootAmount
                            #no items in inv
                            if not inv:
                                inv.append({"Item": item[1], "Amt": lootAmount})
                            else:
                                #search for item in list
                                for invItem in inv:
                                    if invItem["Item"] == item[1]:
                                        invItem["Amt"] += lootAmount
                                        break
                                else:
                                    inv.append({"Item": item[1], "Amt": lootAmount})
                            Parent.SendTwitchMessage("{} mined {} {}.".format(data.User.lower(), lootAmount, item[1]))
                    if gotLoot == False:
                        dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                        Parent.SendTwitchMessage("{} didn't get any loot. Better luck next time. +5 exp".format(data.User.lower()))
                    else:
                        dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                        dbCursor.execute("UPDATE inv SET items = ? WHERE charid = ?", (json.dumps(inv),dbChar[0]))
                        Parent.SendTwitchMessage("{} finished mining. +{} exp".format(data.User.lower(), expGained))
                    #commit changes and close connection
                    dbConnection.commit()
                    dbConnection.close()
                except sqlite3.Error as error:
                    Parent.SendTwitchMessage(str(error))
                    dbConnection.close()
                HasLeveled(data.User.lower())
            #chop wood
            elif args[1].lower() == "chop":
                Parent.SendTwitchMessage("Attempting to chop some wood.")
                #connect to db
                dbConnection = sqlite3.connect(g_RPGdb)
                dbCursor = dbConnection.cursor()
                #get char info
                try:
                    dbCursor.execute("SELECT * FROM chars WHERE user = ?", (data.User.lower(),))
                    dbChar = dbCursor.fetchone()
                    dbCursor.execute("SELECT * FROM stats WHERE charid = ?", (dbChar[0],))
                    dbStats = dbCursor.fetchone()
                    dbCursor.execute("SELECT items FROM inv WHERE charid = ?", (dbChar[0],))
                    dbInv = dbCursor.fetchone()[0]
                    #parse inv
                    inv = json.loads(dbInv)
                    #get list of possible loot
                    dbCursor.execute("SELECT * FROM items WHERE type = ?", ("chop",))
                    dbItems = dbCursor.fetchall()
                    expGained = 5
                    gotLoot = False
                    #iterate through loot
                    for item in dbItems:
                        #determine loot chance
                        lootChance = (item[3] / (1.3 - random.random())) + (dbStats[3] / (100 - random.random())) + (dbStats[4] / (100 - random.random()))
                        if lootChance > 1:
                            gotLoot = True
                            #determine amount of loot
                            lootAmount = int(math.ceil((lootChance - 1) * 10) + random.randint(0, 10))
                            expGained += 5 * lootAmount
                            #no items in inv
                            if not inv:
                                inv.append({"Item": item[1], "Amt": lootAmount})
                            else:
                                #search for item in list
                                for invItem in inv:
                                    if invItem["Item"] == item[1]:
                                        invItem["Amt"] += lootAmount
                                        break
                                else:
                                    inv.append({"Item": item[1], "Amt": lootAmount})
                            Parent.SendTwitchMessage("{} chopped {} {}.".format(data.User.lower(), lootAmount, item[1]))
                    if gotLoot == False:
                        dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                        Parent.SendTwitchMessage("{} didn't get any loot. Better luck next time. +5 exp".format(data.User.lower()))
                    else:
                        dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                        dbCursor.execute("UPDATE inv SET items = ? WHERE charid = ?", (json.dumps(inv),dbChar[0]))
                        Parent.SendTwitchMessage("{} finished chopping. +{} exp".format(data.User.lower(), expGained))
                    #commit changes and close connection
                    dbConnection.commit()
                    dbConnection.close()
                except sqlite3.Error as error:
                    Parent.SendTwitchMessage(str(error))
                    dbConnection.close()
                HasLeveled(data.User.lower())
            #catch fish
            elif args[1].lower() == "fish":
                Parent.SendTwitchMessage("Attempting to catch some fish.")
                #connect to db
                dbConnection = sqlite3.connect(g_RPGdb)
                dbCursor = dbConnection.cursor()
                #get char info
                try:
                    dbCursor.execute("SELECT * FROM chars WHERE user = ?", (data.User.lower(),))
                    dbChar = dbCursor.fetchone()
                    dbCursor.execute("SELECT * FROM stats WHERE charid = ?", (dbChar[0],))
                    dbStats = dbCursor.fetchone()
                    dbCursor.execute("SELECT items FROM inv WHERE charid = ?", (dbChar[0],))
                    dbInv = dbCursor.fetchone()[0]
                    #parse inv
                    inv = json.loads(dbInv)
                    #get list of possible loot
                    dbCursor.execute("SELECT * FROM items WHERE type = ?", ("fish",))
                    dbItems = dbCursor.fetchall()
                    expGained = 5
                    gotLoot = False
                    #iterate through loot
                    for item in dbItems:
                        #determine loot chance
                        lootChance = (item[3] / (1.3 - random.random())) + (dbStats[4] / (100 - random.random())) + (dbStats[7] / (100 - random.random()))
                        if lootChance > 1:
                            gotLoot = True
                            #determine amount of loot
                            lootAmount = int(math.ceil((lootChance - 1) * 10) + random.randint(0, 10))
                            expGained += 5 * lootAmount
                            #no items in inv
                            if not inv:
                                inv.append({"Item": item[1], "Amt": lootAmount})
                            else:
                                #search for item in list
                                for invItem in inv:
                                    if invItem["Item"] == item[1]:
                                        invItem["Amt"] += lootAmount
                                        break
                                else:
                                    inv.append({"Item": item[1], "Amt": lootAmount})
                            Parent.SendTwitchMessage("{} fished {} {}.".format(data.User.lower(), lootAmount, item[1]))
                    if gotLoot == False:
                        dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                        Parent.SendTwitchMessage("{} didn't get any loot. Better luck next time. +5 exp".format(data.User.lower()))
                    else:
                        dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                        dbCursor.execute("UPDATE inv SET items = ? WHERE charid = ?", (json.dumps(inv),dbChar[0]))
                        Parent.SendTwitchMessage("{} finished fishing. +{} exp".format(data.User.lower(), expGained))
                    #commit changes and close connection
                    dbConnection.commit()
                    dbConnection.close()
                except sqlite3.Error as error:
                    Parent.SendTwitchMessage(str(error))
                    dbConnection.close()
                HasLeveled(data.User.lower())
            #hunt prey
            elif args[1].lower() == "hunt":
                Parent.SendTwitchMessage("Attempting to hunt some prey.")
                #connect to db
                dbConnection = sqlite3.connect(g_RPGdb)
                dbCursor = dbConnection.cursor()
                #get char info
                try:
                    dbCursor.execute("SELECT * FROM chars WHERE user = ?", (data.User.lower(),))
                    dbChar = dbCursor.fetchone()
                    dbCursor.execute("SELECT * FROM stats WHERE charid = ?", (dbChar[0],))
                    dbStats = dbCursor.fetchone()
                    dbCursor.execute("SELECT items FROM inv WHERE charid = ?", (dbChar[0],))
                    dbInv = dbCursor.fetchone()[0]
                    #parse inv
                    inv = json.loads(dbInv)
                    #get list of possible loot
                    dbCursor.execute("SELECT * FROM items WHERE type = ?", ("hunt",))
                    dbItems = dbCursor.fetchall()
                    expGained = 5
                    gotLoot = False
                    #iterate through loot
                    for item in dbItems:
                        #determine loot chance
                        lootChance = (item[3] / (1.3 - random.random())) + (dbStats[3] / (100 - random.random())) + (dbStats[4] / (100 - random.random()))
                        if lootChance > 1:
                            gotLoot = True
                            #determine amount of loot
                            lootAmount = int(math.ceil((lootChance - 1) * 10) + random.randint(0, 10))
                            expGained += 5 * lootAmount
                            #no items in inv
                            if not inv:
                                inv.append({"Item": item[1], "Amt": lootAmount})
                            else:
                                #search for item in list
                                for invItem in inv:
                                    if invItem["Item"] == item[1]:
                                        invItem["Amt"] += lootAmount
                                        break
                                else:
                                    inv.append({"Item": item[1], "Amt": lootAmount})
                            Parent.SendTwitchMessage("{} hunted {} {}.".format(data.User.lower(), lootAmount, item[1]))
                    if gotLoot == False:
                        dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                        Parent.SendTwitchMessage("{} didn't get any loot. Better luck next time. +5 exp".format(data.User.lower()))
                    else:
                        dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                        dbCursor.execute("UPDATE inv SET items = ? WHERE charid = ?", (json.dumps(inv),dbChar[0]))
                        Parent.SendTwitchMessage("{} finished hunting. +{} exp".format(data.User.lower(), expGained))
                    #commit changes and close connection
                    dbConnection.commit()
                    dbConnection.close()
                except sqlite3.Error as error:
                    Parent.SendTwitchMessage(str(error))
                    dbConnection.close()
                HasLeveled(data.User.lower())
            #farm produce
            elif args[1].lower() == "farm":
                Parent.SendTwitchMessage("Attempting to farm some produce.")
                #connect to db
                dbConnection = sqlite3.connect(g_RPGdb)
                dbCursor = dbConnection.cursor()
                #get char info
                try:
                    dbCursor.execute("SELECT * FROM chars WHERE user = ?", (data.User.lower(),))
                    dbChar = dbCursor.fetchone()
                    dbCursor.execute("SELECT * FROM stats WHERE charid = ?", (dbChar[0],))
                    dbStats = dbCursor.fetchone()
                    dbCursor.execute("SELECT items FROM inv WHERE charid = ?", (dbChar[0],))
                    dbInv = dbCursor.fetchone()[0]
                    #parse inv
                    inv = json.loads(dbInv)
                    #get list of possible loot
                    dbCursor.execute("SELECT * FROM items WHERE type = ?", ("farm",))
                    dbItems = dbCursor.fetchall()
                    expGained = 5
                    gotLoot = False
                    #iterate through loot
                    for item in dbItems:
                        #determine loot chance
                        lootChance = (item[3] / (1.3 - random.random())) + (dbStats[5] / (100 - random.random())) + (dbStats[6] / (100 - random.random()))
                        if lootChance > 1:
                            gotLoot = True
                            #determine amount of loot
                            lootAmount = int(math.ceil((lootChance - 1) * 10) + random.randint(0, 10))
                            expGained += 5 * lootAmount
                            #no items in inv
                            if not inv:
                                inv.append({"Item": item[1], "Amt": lootAmount})
                            else:
                                #search for item in list
                                for invItem in inv:
                                    if invItem["Item"] == item[1]:
                                        invItem["Amt"] += lootAmount
                                        break
                                else:
                                    inv.append({"Item": item[1], "Amt": lootAmount})
                            Parent.SendTwitchMessage("{} farmed {} {}.".format(data.User.lower(), lootAmount, item[1]))
                    if gotLoot == False:
                        dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                        Parent.SendTwitchMessage("{} didn't get any loot. Better luck next time. +5 exp".format(data.User.lower()))
                    else:
                        dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                        dbCursor.execute("UPDATE inv SET items = ? WHERE charid = ?", (json.dumps(inv),dbChar[0]))
                        Parent.SendTwitchMessage("{} finished farming. +{} exp".format(data.User.lower(), expGained))
                    #commit changes and close connection
                    dbConnection.commit()
                    dbConnection.close()
                except sqlite3.Error as error:
                    Parent.SendTwitchMessage(str(error))
                    dbConnection.close()
                HasLeveled(data.User.lower())
            #embark on a quest of difficulty 0-10
            elif args[1].lower() == "quest":
                if len(args) < 3:
                    Parent.SendTwitchMessage("{}{}\"!rpg quest <difficulty>\" to go on a quest. Difficulty range is 0-10.".format(data.User.lower(), g_ErrorMsg))
                else:
                    Parent.SendTwitchMessage("Going on a quest of difficulty {}.".format(args[2]))
                #connect to db
                dbConnection = sqlite3.connect(g_RPGdb)
                dbCursor = dbConnection.cursor()
                #get char info
                try:
                    dbCursor.execute("SELECT * FROM chars WHERE user = ?", (data.User.lower(),))
                    dbChar = dbCursor.fetchone()
                    dbCursor.execute("SELECT * FROM stats WHERE charid = ?", (dbChar[0],))
                    dbStats = dbCursor.fetchone()
                    dbCursor.execute("SELECT items FROM inv WHERE charid = ?", (dbChar[0],))
                    dbInv = dbCursor.fetchone()[0]
                    #determine success chance
                    successChance = ((dbChar[2] - 1) / int(args[2])) + (dbStats[3] / (100 - random.random())) + (dbStats[4] / (100 - random.random())) + (dbStats[5] / (100 - random.random())) + (dbStats[6] / (100 - random.random())) + (dbStats[7] / (100 - random.random()))
                    if successChance > 1:
                        #parse inv
                        inv = json.loads(dbInv)
                        #get list of possible loot
                        dbCursor.execute("SELECT * FROM items WHERE type = ? OR type = ?", ("quest", "shop"))
                        dbItems = dbCursor.fetchall()
                        expGained = 5 * int(args[2])
                        gotLoot = False
                        #iterate through loot
                        for item in dbItems:
                            #determine loot chance
                            lootChance = (item[3] / (1.3 - (int(args[2]) / 10) - random.random())) + (dbStats[6] / (100 - random.random())) + (dbStats[7] / (100 - random.random()))
                            if lootChance > 1:
                                gotLoot = True
                                #determine amount of loot
                                lootAmount = int(math.ceil((lootChance - 1) * 10) + random.randint(0, 10))
                                expGained += 5 * lootAmount
                                #no items in inv
                                if not inv:
                                    inv.append({"Item": item[1], "Amt": lootAmount})
                                else:
                                    #search for item in list
                                    for invItem in inv:
                                        if invItem["Item"] == item[1]:
                                            invItem["Amt"] += lootAmount
                                            break
                                    else:
                                        inv.append({"Item": item[1], "Amt": lootAmount})
                                Parent.SendTwitchMessage("{} found {} {}.".format(data.User.lower(), lootAmount, item[1]))
                        if gotLoot == False:
                            dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                            Parent.SendTwitchMessage("{} didn't get any loot. Better luck next time. +5 exp".format(data.User.lower()))
                        else:
                            dbCursor.execute("UPDATE chars SET exp = ? WHERE charid = ?", (dbChar[3] + expGained, dbChar[0]))
                            dbCursor.execute("UPDATE inv SET items = ? WHERE charid = ?", (json.dumps(inv),dbChar[0]))
                            Parent.SendTwitchMessage("{} finished a quest. +{} exp".format(data.User.lower(), expGained))
                        #commit changes
                        dbConnection.commit()
                    else:
                        Parent.SendTwitchMessage("{} failed the quest.".format(data.User.lower()))
                    #close connection
                    dbConnection.close()
                except sqlite3.Error as error:
                    Parent.SendTwitchMessage(str(error))
                    dbConnection.close()
                HasLeveled(data.User.lower())
            #display stats of character
            elif args[1].lower() == "stats":
                #connect to db
                dbConnection = sqlite3.connect(g_RPGdb)
                dbCursor = dbConnection.cursor()
                #get char info
                try:
                    dbCursor.execute("SELECT * FROM chars WHERE user = ?", (data.User.lower(),))
                    dbChar = dbCursor.fetchone()
                    dbCursor.execute("SELECT * FROM stats WHERE charid = ?", (dbChar[0],))
                    dbStats = dbCursor.fetchone()
                    #close connection
                    dbConnection.close()
                except sqlite3.Error as error:
                    Parent.SendTwitchMessage(str(error))
                    dbConnection.close()
                #format and send info
                Parent.SendTwitchMessage("{} is level {} with {} experience, {} str, {} dex, {} vit, {} int, {} luk, and {} unassigned points.".format(data.User.lower(), dbChar[2], dbChar[3], dbStats[3], dbStats[4], dbStats[5], dbStats[6], dbStats[7], dbStats[2]))
                HasLeveled(data.User.lower())
            #assign stat points
            elif args[1].lower() == "assign":
                if len(args) < 4:
                    Parent.SendTwitchMessage("{}{}\"!rpg assign <stat> <amount>\" to assign stat point(s).".format(data.User.lower(), g_ErrorMsg))
                else:
                    #connect to db
                    dbConnection = sqlite3.connect(g_RPGdb)
                    dbCursor = dbConnection.cursor()
                    #get char info
                    try:
                        dbCursor.execute("SELECT * FROM chars WHERE user = ?", (data.User.lower(),))
                        dbChar = dbCursor.fetchone()
                        dbCursor.execute("SELECT * FROM stats WHERE charid = ?", (dbChar[0],))
                        dbStats = dbCursor.fetchone()
                        if int(args[3]) > dbStats[2]:
                            Parent.SendTwitchMessage("Not enough stat points.")
                        elif args[2] == "str":
                            dbCursor.execute("UPDATE stats SET str = ?, points = ? WHERE charid = ?", (dbStats[3] + int(args[3]), dbStats[2] - int(args[3]), dbChar[0]))
                            Parent.SendTwitchMessage("{} assigned {} points to {}.".format(data.User.lower(), args[3], args[2]))
                        elif args[2] == "dex":
                            dbCursor.execute("UPDATE stats SET dex = ?, points = ? WHERE charid = ?", (dbStats[4] + int(args[3]), dbStats[2] - int(args[3]), dbChar[0]))
                            Parent.SendTwitchMessage("{} assigned {} points to {}.".format(data.User.lower(), args[3], args[2]))
                        elif args[2] == "vit":
                            dbCursor.execute("UPDATE stats SET vit = ?, points = ? WHERE charid = ?", (dbStats[5] + int(args[3]), dbStats[2] - int(args[3]), dbChar[0]))
                            Parent.SendTwitchMessage("{} assigned {} points to {}.".format(data.User.lower(), args[3], args[2]))
                        elif args[2] == "int":
                            dbCursor.execute("UPDATE stats SET int = ?, points = ? WHERE charid = ?", (dbStats[6] + int(args[3]), dbStats[2] - int(args[3]), dbChar[0]))
                            Parent.SendTwitchMessage("{} assigned {} points to {}.".format(data.User.lower(), args[3], args[2]))
                        elif args[2] == "luk":
                            dbCursor.execute("UPDATE stats SET luk = ?, points = ? WHERE charid = ?", (dbStats[7] + int(args[3]), dbStats[2] - int(args[3]), dbChar[0]))
                            Parent.SendTwitchMessage("{} assigned {} points to {}.".format(data.User.lower(), args[3], args[2]))
                        else:
                            Parent.SendTwitchMessage("{}{}Valid stats are str, dex, vit, int, luk.".format(data.User.lower(), g_ErrorMsg))
                        #commit changes and close connection
                        dbConnection.commit()
                        dbConnection.close()
                    except sqlite3.Error as error:
                        Parent.SendTwitchMessage(str(error))
                        dbConnection.close()
            #display current inventory along with item worth
            elif args[1].lower() == "inv":
                #connect to db
                dbConnection = sqlite3.connect(g_RPGdb)
                dbCursor = dbConnection.cursor()
                #get char inv
                try:
                    dbCursor.execute("SELECT charid FROM chars WHERE user = ?", (data.User.lower(),))
                    dbCharid = dbCursor.fetchone()[0]
                    dbCursor.execute("SELECT * FROM inv WHERE charid = ?", (dbCharid,))
                    dbInv = dbCursor.fetchone()
                    #close connection
                    dbConnection.close()
                except sqlite3.Error as error:
                    Parent.SendTwitchMessage(str(error))
                    dbConnection.close()
                #format and send info
                dbItems = json.loads(dbInv[3])
                inv = ""
                #check if inv empty
                if not dbItems:
                    inv = "no items"
                #check if inv only has 1 item
                elif len(dbItems) == 1:
                    inv = "{} {}".format(dbItems[0]["Amt"], dbItems[0]["Item"])
                #parse inv and format into string
                else:
                    for item in dbItems:
                        if item == dbItems[-1]:
                            inv += "and {} {}".format(item["Amt"], item["Item"])
                        else:
                            inv += "{} {}, ".format(item["Amt"], item["Item"])
                Parent.SendTwitchMessage("{} has {} gold and {}.".format(data.User.lower(), dbInv[2], inv))
            #enter shop to buy/sell items
            elif args[1].lower() == "shop":
                if len(args) < 3:
                    Parent.SendTwitchMessage("{}{}\"!rpg shop <buy/sell/list> (<item> <amount>)\" to use shop.".format(data.User.lower(), g_ErrorMsg))
                #list shop items and prices
                elif args[2].lower() == "list":
                    #connect to db
                    dbConnection = sqlite3.connect(g_RPGdb)
                    dbCursor = dbConnection.cursor()
                    #get shop items
                    try:
                        dbCursor.execute("SELECT * FROM items WHERE type = ?", ("shop",))
                        dbShopItems = dbCursor.fetchall()
                        items = "The shop is selling "
                        #parse items and format into string
                        for item in dbShopItems:
                            if item == dbShopItems[-1]:
                                items += "and {} for {} gold.".format(item[1], item[4])
                            else:
                                items += "{} for {} gold, ".format(item[1], item[4])
                        Parent.SendTwitchMessage(items)
                        #close connection
                        dbConnection.close()
                    except sqlite3.Error as error:
                        Parent.SendTwitchMessage(str(error))
                        dbConnection.close()
                elif len(args) < 5:
                    Parent.SendTwitchMessage("{}{}\"!rpg shop <buy/sell> <item> <amount>\" to buy/sell item(s).".format(data.User.lower(), g_ErrorMsg))
                #add item to inv and remove money
                elif args[2].lower() == "buy":
                    #connect to db
                    dbConnection = sqlite3.connect(g_RPGdb)
                    dbCursor = dbConnection.cursor()
                    #get user info
                    try:
                        dbCursor.execute("SELECT charid FROM chars WHERE user = ?", (data.User.lower(),))
                        dbCharid = dbCursor.fetchone()[0]
                        dbCursor.execute("SELECT * FROM inv WHERE charid = ?", (dbCharid,))
                        dbInv = dbCursor.fetchone()
                        #get shop items
                        dbCursor.execute("SELECT * FROM items WHERE item = ?", (args[3],))
                        if dbCursor.fetchone() == None:
                            Parent.SendTwitchMessage("{} is not an item for sale in the shop.".format(args[3]))
                        else:
                            dbShopItem = dbCursor.fetchone()
                            cost = dbShopItem[4] * int(args[4])
                            if cost > dbInv[2]:
                                Parent.SendTwitchMessage("Insufficient funds.")
                            else:
                                inv = json.loads(dbInv[3])
                                if not inv:
                                    inv.append({"Item": dbShopItem[1], "Amt": int(args[4])})
                                else:
                                    #search for item in list
                                    for invItem in inv:
                                        if invItem["Item"] == dbShopItem[1]:
                                            invItem["Amt"] += int(args[4])
                                            break
                                    else:
                                        inv.append({"Item": dbShopItem[1], "Amt": int(args[4])})
                                dbCursor.execute("UPDATE inv SET items = ?, money = ? WHERE charid = ?", (json.dumps(inv), dbInv[2] - cost, dbCharid))
                                Parent.SendTwitchMessage("{} bought {} {} for {} gold.".format(data.User.lower(), args[4], args[3], str(cost)))
                        #commit changes and close connection
                        dbConnection.commit()
                        dbConnection.close()
                    except sqlite3.Error as error:
                        Parent.SendTwitchMessage(str(error))
                        dbConnection.close()
                #remove item from inv and add money
                elif args[2].lower() == "sell":
                    #connect to db
                    dbConnection = sqlite3.connect(g_RPGdb)
                    dbCursor = dbConnection.cursor()
                    #get user info
                    try:
                        dbCursor.execute("SELECT charid FROM chars WHERE user = ?", (data.User.lower(),))
                        dbCharid = dbCursor.fetchone()[0]
                        dbCursor.execute("SELECT * FROM inv WHERE charid = ?", (dbCharid,))
                        dbInv = dbCursor.fetchone()
                        #get item info
                        dbCursor.execute("SELECT * FROM items WHERE item = ?", (args[3],))
                        dbItem = dbCursor.fetchone()
                        if dbItem == None:
                            Parent.SendTwitchMessage("{} does not exist.".format(args[3]))
                        else:
                            inv = json.loads(dbInv[3])
                            if not inv:
                                Parent.SendTwitchMessage("No items in inv.")
                            for invItem in inv:
                                #check if item matches and if there are enough items to sell
                                if invItem["Item"] == args[3]:
                                    if invItem["Amt"] < int(args[4]):
                                        Parent.SendTwitchMessage("Not enough items to sell.")
                                        break
                                    else:
                                        invItem["Amt"] -= int(args[4])
                                        break
                            for item in inv[:]:
                                if item["Amt"] == 0:
                                    inv.remove(item)
                            profit = dbItem[5] * int(args[4])
                            dbCursor.execute("UPDATE inv SET items = ?, money = ? WHERE charid = ?", (json.dumps(inv), dbInv[2] + profit, dbCharid))
                            Parent.SendTwitchMessage("{} sold {} {} for {} gold.".format(data.User.lower(), args[4], args[3], profit))
                            #commit changes
                            dbConnection.commit()
                        #close connection
                        dbConnection.close()
                    except sqlite3.Error as error:
                        Parent.SendTwitchMessage(str(error))
                        dbConnection.close()
                else:
                    Parent.SendTwitchMessage("{}{}\"!rpg shop list\" lists the shop's items and costs.".format(data.User.lower(), g_ErrorMsg))
                    Parent.SendTwitchMessage("\"!rpg shop <buy/sell> <item> <amount>\" to buy/sell item(s).")
            else:
                Parent.SendTwitchMessage("{}{}\"!rpg\" help to get started.".format(data.User.lower(), g_ErrorMsg))
            #update cooldown
            global g_LastUsed
            g_LastUsed = datetime.datetime.now()

#Tick
def Tick():
    return

#Cooldown
def IsOnCooldown():
    return (datetime.datetime.now() - g_LastUsed).total_seconds() < g_CooldownTime

#Leveling
def HasLeveled(user):
    #connect to db
    dbConnection = sqlite3.connect(g_RPGdb)
    dbCursor = dbConnection.cursor()
    #get char info
    try:
        dbCursor.execute("SELECT * FROM chars WHERE user = ?", (user,))
        dbChar = dbCursor.fetchone()
        dbCursor.execute("SELECT * FROM stats WHERE charid = ?", (dbChar[0],))
        dbStats = dbCursor.fetchone()
        #calculate level based on exp
        calcLevel = int(1 + math.floor(0.08 * math.sqrt(dbChar[3])))
        #determine if level has changed
        if dbChar[2] < calcLevel:
            dbCursor.execute("UPDATE chars SET level = ? WHERE charid = ?", (calcLevel, dbChar[0]))
            dbCursor.execute("UPDATE stats SET points = ? WHERE charid = ?", (dbStats[2] + 5, dbChar[0]))
            Parent.SendTwitchMessage("{} is now level {}.".format(user, calcLevel))
            #commit changes and close connection
            dbConnection.commit()
            dbConnection.close()
        else:
            dbConnection.close()
    except sqlite3.Error as error:
        Parent.SendTwitchMessage(str(error))
        dbConnection.close()
