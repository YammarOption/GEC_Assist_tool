import PySimpleGUI as sg
import json
import re
import os.path as op
next_color={"red":"blue","blue":"white","white":"red"}
skiptrainer=["rival_Optional","rival"]

def create_route_window(route,itemsinroute,trainerinroute,eventsinroute):
    file="routes/"+route+".json"
    events=[]
    trainers=[]
    items=[]
    layout=[]
    with open(file) as db:
        data = json.load(db)
        events = data["events"]
        trainers = data["trainers"]
        items = data["items"]
    floors= list(trainers.keys() | events.keys() | items.keys())
    for floor in floors:
        if floor == "0":
            name =sg.Text("Overworld",key="floor",font=("Arial",25,"bold"),expand_x=True,expand_y=True,justification='center')
        else: name =sg.Text(floor.upper(),key="floor",font=("Arial",25,"bold"),expand_x=True,expand_y=True,justification='center')
        layout.append([name])
        
        if floor in items and len(items[floor])>0:
            layout.append([sg.Text("Items",font=("Arial",20,"bold"),expand_x=True,expand_y=True,justification='left')])
            for j in items[floor]:
                key = "ITEM-"+j+"_"
                cbox=sg.Checkbox(text=j, key=key,default=key in itemsinroute,enable_events=True)
                layout.append(
                [cbox]
                )   

        prev_name=""
        if floor in trainers and len(trainers[floor])>0:
            layout.append([sg.Text("Trainers",font=("Arial",20,"bold"),expand_x=True,expand_y=True,justification='left')])
            for j in trainers[floor]:
                if j["name"]  not in skiptrainer or  prev_name != j["name"]:
                    key = "TRAINER-"+j["name"]+"_"
                    cbox=sg.Checkbox(text="", key=key,default=key in trainerinroute,enable_events=True)
                    tr=[cbox,
                        sg.Text(j["name"].upper())]
                    layout.append(tr)
                    prev_name = j["name"]
                mon=[]
                for i in range(len(j["mons"])):
                    mon.append(sg.T(""))
                    mon.append(sg.Image(filename="Sprites/mons/"+j["mons"][i].lower()+".png",expand_x=True))
                levels=[]
                if len(j["levels"])>1:
                    for i in range(len(j["mons"])):
                        levels.append(sg.Text(str(j["levels"][i]),expand_x=True,justification='center',font=("Arial",12,"bold")))
                else:
                    for i in range(len(j["mons"])):
                        levels.append(sg.Text(str(j["levels"][0]),expand_x=True,justification='center',font=("Arial",12,"bold")))
                layout.append(mon)
                layout.append(levels)

        if floor in events and len(events[floor])>0:
            layout.append([sg.Text("Events",font=("Arial",20,"bold"),expand_x=True,expand_y=True,justification='left')])
            for j in events[floor]:
                key = "EVENT-"+j+"_"
                cbox=sg.Checkbox(text=j, key=key,default=key in eventsinroute,enable_events=True)
                layout.append([cbox])
    select_route = [sg.Combo(values=routes,key="ROUTES",default_value=route,enable_events=True)]
    return sg.Window("GEC-Route Assist",layout=[select_route,[sg.Column(layout, scrollable=True,expand_y=True,expand_x=True)]],resizable=True,finalize=True)
    
monNO=0
dex = []
itemsNO = 0
items=()
movesNO = 0
moves = []
miscNO = 0
vs_NO=0
routes=[]
with open("routes/Summary.json") as db:
    data = json.load(db)
    monNO = data["MonsNO"]
    dex = data["Monset"]
    itemsNO = data["ItemsNO"]
    items = set(data["ItemList"])
    miscNO = data["Miscs"]
    movesNO=data["MovesNO"]
    moves = sorted(data["Moves"])
    vs_NO = data["VSNO"]
    routes=sorted(data["Routes"])
#print(str(len(items)))
datafile=False
if op.isfile("Data/data.json"):
    with open("Data/data.json") as savefile:
        jload=json.load(savefile)
        itemset=jload["itemset"]
        moveset=jload["moveset"]
        dexset=jload["dexset"]
        eventset=jload["eventset"]
        curr_route=jload["curr_route"]
        itemsinRoute=jload["itemsinRoute"]
        trainerinRoute=jload["trainerinRoute"]
        items_counter=jload["itemNO"]
        misc_counter=jload["miscNO"]
        current_moves_NO=jload["movesNO"]
        dex_counter=jload["dexNO"]
        trainer_counter=jload["trainerNO"]

else:
    itemset=[]
    moveset=[]
    dexset={i:"white" for i in dex}
    eventset = []
    curr_route="pallettown"
    itemsinRoute={}
    itemsinRoute[curr_route]=[]
    trainerinRoute={}
    trainerinRoute[curr_route]=[]
    items_counter=0
    misc_counter=0
    trainer_counter=0
    dex_counter=0
    current_moves_NO=0


####################
## COUNTERS ROW
img_row = [
    sg.Image(key="BALL",filename="Sprites/ball.png",expand_x=True,expand_y=True),
    sg.Image(key="ITEMS",filename="Sprites/potion.png",expand_x=True,expand_y=True,enable_events=True),
    sg.Image(key="VS",filename="Sprites/VS_Seeker.png",expand_x=True,expand_y=True),
    sg.Image(key="MOVES",filename="Sprites/moves.png",expand_x=True,expand_y=True),
    sg.Image(key="MISC",filename="Sprites/leftovers.png",expand_x=True,expand_y=True),
]

counter_row = [
    sg.Text(str(dex_counter)+"/"+str(monNO),key="MON_COUNTER",font=("Arial",25,"bold"),expand_x=True,expand_y=True,justification='center'),
    sg.Column([[sg.Button(key="MINUS_ITEM",button_text="-"),
     sg.Text(str(items_counter)+"/"+str(itemsNO),key="ITEMS_COUNTER",font=("Arial",25,"bold"),justification='center'),
     sg.Button(key="PLUS_ITEM",button_text="+")]]),
    sg.Text(str(trainer_counter)+"/"+str(vs_NO),key="TRAINER_COUNTER",font=("Arial",25,"bold"),expand_x=True,expand_y=True,justification='center'),
    sg.Text(str(current_moves_NO)+"/"+str(movesNO),key="MOVES_COUNTER",font=("Arial",25,"bold"),expand_x=True,expand_y=True,justification='center'),
    sg.Text(str(misc_counter)+"/"+str(miscNO),key="MISC_COUNTER",font=("Arial",25,"bold"),expand_x=True,expand_y=True,justification='center')
]

### POKEDEX #######

#test matrix pokemon
Images = list()
#files = sorted(os.listdir("Sprites/mons"))
curr_row=[]
count=0
for img in dex:
    if count >10:
        count=0
        Images.append(curr_row)
        curr_row=[]
    pic=sg.Image(key=img,filename="Sprites/mons/"+img.lower()+".png", enable_events=True,background_color=dexset[img])
    pic.currentcolor=dexset[img]
    curr_row.append(pic)
    
    count+=1
Images.append(curr_row)
col = sg.Column(Images,key="Mon_col", scrollable=True,background_color='black',expand_y=True)

#######
###### MOVES LISTBOX
move_list = [
    [sg.Text("MOVE LIST:",key="MOVE_LIST",font=("Arial",25,"bold"))]
]
for j in moves:
    key = "MOVE-"+j
    move_list.append([
      sg.Checkbox(
        text=j, key=key,default=key in moveset ,enable_events=True
      )
    ])
move_col = sg.Column(move_list,scrollable=True,key="move_col",expand_y=True,expand_x=True)
#########
# LAYOUT 1
window = sg.Window("GEC-Assist Tool",layout=[img_row,counter_row,[sg.HSeparator()], [col,move_col]],resizable=True,finalize=True)

#########
# LAYOUT 2

window2 = create_route_window(curr_route,itemsinRoute[curr_route],trainerinRoute[curr_route],eventset)
save={}
while True:
    windowE,event,vals = sg.read_all_windows()
    #print(event)
    if event == "Exit" or event == sg.WIN_CLOSED:
        #save all
        save["itemset"]=itemset
        save["moveset"]=moveset
        save["dexset"]=dexset
        save["eventset"]=eventset
        save["curr_route"]=curr_route
        save["itemsinRoute"]=itemsinRoute
        save["trainerinRoute"]=trainerinRoute
        save["trainerNO"]=trainer_counter
        save["itemNO"]=items_counter
        save["miscNO"]=misc_counter
        save["movesNO"]=current_moves_NO
        save["dexNO"]=dex_counter
        with open("Data/data.json",'w') as savefile:
            json.dump(fp=savefile,indent=4,obj=save,default=list)
        break

    elif event.startswith("MOVE"):
        if window[event].get():
            current_moves_NO+=1
            moveset.append(event)

        else:
            current_moves_NO-=1
            moveset.remove(event)
        window["MOVES_COUNTER"].update(str(current_moves_NO)+"/"+str(movesNO))

    elif event == "ITEMS":
        string=""
        missing=set(items)-set(itemset)
        for i in sorted(missing):
            string=string+i+"\n"
        sg.popup_scrolled(string,title="Missing Items",)

    elif event == "PLUS_ITEM":
        items_counter+=1
        window["ITEMS_COUNTER"].update(str(items_counter)+"/"+str(itemsNO))

    elif event == "MINUS_ITEM":
        items_counter-=1
        window["ITEMS_COUNTER"].update(str(items_counter)+"/"+str(itemsNO))

    elif event.startswith("ITEM-"):
        itemname = re.findall(r'\-([^]]*)\_', event)[0]
        #print(itemname)
        if windowE[event].get():
            items_counter+=1
            itemset.append(itemname.lower())
        else:
            items_counter-=1
            itemset.remove(itemname.lower())
        itemsinRoute[curr_route].append(event)
        window["ITEMS_COUNTER"].update(str(items_counter)+"/"+str(itemsNO))

    elif event.startswith("EVENT-"):
        if windowE[event].get():
            misc_counter+=1
            eventset.append(event)
        else:
            misc_counter-=1
            eventset.remove(event)
        window["MISC_COUNTER"].update(str(misc_counter)+"/"+str(miscNO))

    elif event.startswith("TRAINER-"):
        if windowE[event].get():
            trainer_counter+=1
            trainerinRoute[curr_route].append(event)

        else:
            trainer_counter-=1
            trainerinRoute[curr_route].remove(event)
        window["TRAINER_COUNTER"].update(str(trainer_counter)+"/"+str(vs_NO))

    elif event == "ROUTES":
        curr_route = vals[event]
        if event not in itemsinRoute:
            itemsinRoute[curr_route]=[]
        if event not in trainerinRoute:
            trainerinRoute[curr_route]=[]
        window2.close()
        window2 = create_route_window(curr_route,itemsinRoute[curr_route],trainerinRoute[curr_route],eventset)
    
    else: 
        color=next_color[window[event].currentcolor]
        if color == 'red':
            dex_counter+=1
        elif color == 'blue':dex_counter -=1
        window[event].currentcolor= color
        window[event].Widget.config(background=color)
        window[event].Widget.config(highlightbackground=color)
        window[event].Widget.config(highlightcolor=color)
        dexset[event]=color
        window["MON_COUNTER"].update(str(dex_counter)+"/"+str(monNO))
        
window.close()
window2.close()