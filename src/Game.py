import json
import os.path as op
MON_PER_ROW=9 
ITEMS_PER_ROW=10 

class Game :

    '''
    Class constructor. Stores all info related to game progreess
    :param str game: the game used
    '''
    def __init__(self,game):
        self.name = game
        self.curr_route=""
        self.MON_PER_ROW=MON_PER_ROW
        self.ITEMS_PER_ROW=ITEMS_PER_ROW
        if op.isfile("Datapack/data.json"):
            with open("Datapack/data.json") as savefile:
                jload=json.load(savefile)
                self.total_checked_elements=jload["checked_elements"]
                self.checkedMoves=jload["moveset"]
                self.checkedMons = jload["checkedmons"]
                self.curr_route=jload["curr_route"]
                self.checked_elements_per_route=jload["checked_elements_per_route"]
                self.trainerinRoute=jload["trainerinRoute"]
                self.items_counter=jload["itemNO"]
                self.event_counter=jload["miscNO"]
                self.trainer_counter=jload["trainerNO"]
                self.dex_counter=jload["dexNO"]
                self.moves_counter=jload["movesNO"]
        else:
            self.checkedMons={}
            self.total_checked_elements={}
            self.checkedMoves=[]
            self.checked_elements_per_route={}
            self.trainerinRoute={}
            self.items_counter=0
            self.event_counter=0
            self.trainer_counter=0
            self.dex_counter=0
            self.moves_counter=0
        with open("Datapack/routes/Summary.json") as db:
            data = json.load(db)
            self.totalMons = data["MonsNO"]
            if "Mons_per_row" in data:
                self.MON_PER_ROW=data["Mons_per_row"]  
            if "Items_per_row" in data:
                self.ITEMS_PER_ROW=data["Items_per_row"]        
            self.dexList = data["Monset"]
            self.totalItems = data["ItemsNO"]
            self.totalEvents = data["MiscsNO"]
            self.totalMoves=data["MovesNO"]
            self.totalTrainers = data["VSNO"]
            self.itemList = data["ItemList"]
            self.movesList = sorted(data["Moves"])
            if not self.curr_route:
                self.curr_route=data["Starting_route"]
            self.routes=sorted(data["Routes"])
            if len(self.checkedMons) == 0:
                self.checkedMons={i.upper():0 for i in self.dexList}
            if len (self.total_checked_elements)==0:
                for i in self.itemList:
                    item =list(i.keys())[0]
                    if not item == "blank" :
                        #Couple with #current item and #max item
                        self.total_checked_elements[item.replace(" ","").upper()]=[0,i[item][1]]
        if len(self.checked_elements_per_route)==0: self.checked_elements_per_route = {i:[] for i in self.routes}
        if len(self.trainerinRoute)==0: self.trainerinRoute = {i:[] for i in self.routes}
    
    '''
    Save the tracker's progress to a json file
    '''

    def save(self):
        save={}
        save["checked_elements"]=self.total_checked_elements
        save["moveset"]=self.checkedMoves
        save["checkedmons"]=self.checkedMons
        save["curr_route"]=self.curr_route
        save["checked_elements_per_route"]=self.checked_elements_per_route
        save["trainerinRoute"]=self.trainerinRoute
        save["trainerNO"]=self.trainer_counter
        save["itemNO"]=self.items_counter
        save["miscNO"]=self.event_counter
        save["dexNO"]=self.dex_counter
        save["movesNO"]=self.moves_counter
        with open("Datapack/data.json",'w') as savefile:
            json.dump(fp=savefile,indent=4,obj=save,default=list)

    '''
    Update pokedex status based on event from the main window
    :param str id: the pokémon's id
    :param bool update: if we must ad or remove the pokemon from the dex
    '''
    def updateMons(self,id:str,update):
        if update and not (self.checkedMons[id]==1):
            self.dex_counter+=1
        elif not update and self.checkedMons[id]==1: self.dex_counter=max(self.dex_counter-1,0)
   
    '''
    Update moves list status based on event from the main window
    :param str id: the move's id
    :param bool update: if we must ad or remove the m0ve from the dex
    '''

    def updateMoves(self,move,state):
        if state and move not in self.checkedMoves:
            self.moves_counter += 1
            self.checkedMoves.append(move)
        elif not state and move in self.checkedMoves:
            self.moves_counter -= 1
            self.checkedMoves.remove(move)
    
    '''
    Update trainer list status based on event from the main window
    :param bool state: if we must ad or remove the trainer from the dex
    :param str code: the trainer's code
    '''

    def updateTrainer(self,state,code):
        if state:
            self.trainer_counter += 1
            self.trainerinRoute[self.curr_route].append(code)
        else :
            self.trainer_counter -= 1
            self.trainerinRoute[self.curr_route].remove(code)

    '''
    Update item list status based on event from the main window
    :param str id: the item's id
    :param str route_id: the item's id within a specific route. Could be empty if the item is not related in any route
    :param str route: the item's id within a specific route
    :param bool update: if we must ad or remove the id from the dex
    '''
    def updateItems(self,id,route_id,route,state):
        if state:  ## NEW CHECK: UPDATE COUNTERS, eventually show label
            self.items_counter+=1
            self.total_checked_elements[id][0]+=1
            if route_id: #some element are not bound to a specific route. Therefore we need to check
                self.checked_elements_per_route[route].append(route_id)
            ## Update label
        else:
            self.items_counter-=1
            self.total_checked_elements[id][0]-=1
            if route_id:
                self.checked_elements_per_route[route].remove(route_id)
    
    '''
    Update event list's status based on event from the main window
    :param str id: the event's id
    :param str route_id: the event's id within a specific route. Could be empty if the event is not related in any route
    :param str route: the item's id within a specific route
    :param bool update: if we must ad or remove the id from the dex
    '''
    def updateEvents(self,id,route_id,route,state):
        if state:  ## NEW CHECK: UPDATE COUNTERS, eventually show label
            self.event_counter+=1
            self.total_checked_elements[id][0]+=1
            if route_id: #some element are not bound to a specific route. Therefore we need to check
                self.checked_elements_per_route[route].append(route_id)
            ## Update label
        else:
            self.event_counter-=1
            self.total_checked_elements[id][0]-=1
            if route_id:
                self.checked_elements_per_route[route].remove(route_id)
    '''
    Check if exists an event connected to obtaining a certain pokemon
    :param str mon: the pokémon name to look up event for
    :return: True if the pokémon has a event associated with its catch
    '''
    def checkEventForMon(self,mon:str):
        return ""

    '''
    Check if exists an event connected to obtaining a certain item
    :param str item: the item name to look up event for
    :return: True if the pokémon has a event associated with its catch
    '''
    def checkEventForItem(self,id:str):
        return ""

    '''
    Return an event ID connected to obtaining a certain pokemon
    :param str mon: the pokémon name to look up event for
    :return: the event id associated with the pokémon, or empty string if any
    '''
    def getEventForMon(self,mon:str):
        return ""
    
    '''
    Return an event ID connected to obtaining a certain item
    :param str item: the item name to look up event for
    :return: the event id associated with the item, or empty string if any
    '''
    def getEventForItem(self,id:str):
        return ""
    
    '''
    Change an item ID to match another. Used when multiple events/item concurr towards the same goal
    :param str item: the item rename
    :return: the event id associated with the item, or empty string if any
    '''
    def renameElement(self,item:str):
        pass

    '''
    Return the layout to use for the game monitor layout as list of string to use in Qlabels
    :return: a list of element to insert in the 
    '''
    def getGameMonitorlayout(self):
        pass

    '''
    Return a list of update string to use to update the game monitor layout
    :return: a list of string used to update the game monitor layout
    '''
    def updateGameMonitorlayout(self,data:str):
        print("ERROR")

#########################################
########## GEN  1########################
#########################################
'''
Implements Game class for Gen 1 games
'''
class GS_Gen1 (Game):
    def __init__(self, game):
        super().__init__(game)

    def updateMons(self, id, update):
        super().updateMons(id, update)

    def checkEventForMon(self,mon:str):
        return  mon.startswith("SNORLAX") or\
            mon.startswith("MEW") or\
            mon.startswith("MEWTWO") or\
            mon.startswith("ARTICUNO") or\
            mon.startswith("ZAPDOS") or\
            mon.startswith("MOLTRES") 
    
    
    def getEventForMon(self,mon:str):
        if mon.startswith("SNORLAX"):return "SNORLAX"
        if mon.startswith("MEWTWO"):return "MEWTWO"
        if mon.startswith("MEW"):return "GLITCHMEW"
        if mon.startswith("ARTICUNO"):return "ARTICUNO"
        if mon.startswith("ZAPDOS"):return "ZAPDOS"
        if mon.startswith("MOLTRES"):return "MOLTRES"
        return ""
        
    def renameElement(self, item:str):
        if item.startswith("GETTONI"):
            return "GETTONI"
        if "TRAPPOLA" in item:
            return "VOLTORBTRAPPOLA"
        return item
    
    def getGameMonitorlayout(self):
        return[]

    def updateGameMonitorlayout(self,data:str):
        return []
    
#########################################
########## GEN 2 ########################
#########################################
'''
Implements Game class for Gen 2 games
'''
class GS_Gen2 (Game):
    def __init__(self, game):
        self.unownCount=0
        self.unownThresh = False
        self.password = 0
        super().__init__(game)

    def updateMons(self, id, update):
        super().updateMons(id, update)
        if update and not (self.checkedMons[id]==1) and id.startswith("UNOWN"):
            self.unownThresh = self.unownCount==25
            self.unownCount+=1
        elif not update and self.checkedMons[id]==1 and id.startswith("UNOWN"):
            self.unownThresh = self.unownCount==26 
            self.unownCount-=1

    def checkEventForMon(self,mon:str):
        return  (mon.startswith("UNOWN") and self.unownThresh) or\
            mon.startswith("ENTEI") or\
            mon.startswith("RAIKOU") or\
            mon.startswith("SUICUNE") or\
            mon.startswith("SUDOWOODO") or\
            mon.startswith("LAPRAS") or\
            mon.startswith("SNORLAX") or\
            mon.startswith("LUGIA") or\
            mon.startswith("HO-OH") or\
            mon.startswith("MEW") or\
            mon.startswith("CELEBI") 
    
    def checkEventForItem(self,id:str):
        return id.startswith("MAMMA-")
    
    def getEventForMon(self,mon:str):
        if mon.startswith("UNOWN"):return "26UNOWN"
        if mon.startswith("ENTEI"):return "ENTEI"
        if mon.startswith("RAIKOU"):return "RAIKOU"
        if mon.startswith("SUICUNE"):return "SUICUNE"
        if mon.startswith("SUDOWOODO"):return "SUDOWOODO"
        if mon.startswith("LAPRAS"):return "LAPRAS"
        if mon.startswith("SNORLAX"):return "SNORLAX"
        if mon.startswith("LUGIA"):return "LUGIA"
        if mon.startswith("HO-OH"):return "HO-OH"
        if mon.startswith("MEW"):return "MEW"
        if mon.startswith("CELEBI"):return "CELEBI"
        return ""
    
    def getEventForItem(self, id:str):
        if not id.startswith("MAMMA-"):
            return ""
        return "STRUMENTIMAMMA"
    
    def renameElement(self, item:str):
        if item.startswith("GETTONI"):
            return "GETTONI"
        if item.startswith("MAMMA-"):
            return item.replace("MAMMA-","")
        if item.startswith("DECO-"):
            return "DECORAZONI"
        if item.startswith("TRAPPOLA"):
            return "POK\u00c9MONTRAPPOLA"
        if item.startswith("PUZZLE"):
            return "PUZZLEROVINE"
        if item.startswith("NUMEROTELEFONO"):
            return "NUMERIDITELEFONO"
        if item.startswith("FRATELLISETTIMANA"):
            return "FRATELLISETTIMANA"
        if item.endswith("INVIATO"):
            return "MESSAGGIALPC"
        return item
    
    def getGameMonitorlayout(self):
        #return["Datapack/Sprites/money.png","??","Datapack/Sprites/ID.png","??","Datapack/Sprites/password.png","??"]
        return["Datapack/Sprites/money.png","??","Datapack/Sprites/ID.png","??","Datapack/Sprites/PWD.png","??"]

    def updateGameMonitorlayout(self,data:str):
        values = data.split("@")
        updateValue=[]
        name=""
        tID=0
        money=0
        for value in values:
            if value.startswith("MONEY"):
                money = int(value.replace("MONEY:",""),16)
                updateValue.append("{:06d}".format(money))
            if value.startswith("ID"):
                tID = int(value.replace("ID:",""),16)
                updateValue.append("{:05d}".format(tID))
            if value.startswith("NAME"):
                name=value.replace("NAME:","")
        password=0
        x = 0
        if len(name) >= 2:
            while x < len(name):
                password += int(name[x]+name[x+1],16)
                x+=2
        password += ((tID >> 8) + (tID & 0xFF) + ((money >> 16) & 0xFF) + ((money >> 8) & 0xFF) + (money & 0xFF))
        if password == 0:
            updateValue.append("{:05d}".format(self.password))
        else:
            self.password=password
            updateValue.append("{:05d}".format(password))
        return updateValue


class GameFactory:

    def getGame(self, game:str):
        if game.upper() == "RBG":
            return GS_Gen1(game)
        if game.upper() == "OA":
            return GS_Gen2(game)

