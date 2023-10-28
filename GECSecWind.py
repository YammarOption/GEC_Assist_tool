from PyQt5.QtWidgets import (QWidget,QVBoxLayout, QStackedLayout, QMainWindow, QScrollArea, 
                            QLabel, QCheckBox, QSplitter, QComboBox)
from PyQt5.QtGui import  QPixmap, QCloseEvent
from PyQt5.QtCore import Qt
from QTExtra import FlowLayout,MyCheckbox 

import json

skiptrainer=["rival_Optional","rival"]



class GECSecwindow(QMainWindow):
    def __init__(self,parent,moves,checkedmoves,routes,currentRoute,itemsinroute,trainerinroute):
        super(GECSecwindow, self).__init__()
        self.setWindowTitle("GEC Tool 2.0 AA")
        self.parent = parent
        self.moves = moves
        self.checkedMoves = checkedmoves
        self.routes = routes
        #######
        ###### MOVES LISTBOX
        ######
        moveWidget = QWidget()
        moveWidgetLayout = QVBoxLayout()
        moveheader = QLabel("Move List")
        moveWidgetLayout.addWidget(moveheader)
        movelist=QWidget()
        movelistLayout=QVBoxLayout()
        chlist=[]
        for move in moves:  
            Chbox = QCheckBox(move)
            if move in self.checkedMoves:
                Chbox.setChecked(True)
            Chbox.stateChanged.connect(self.updateMoves)
            chlist.append(Chbox)
            movelistLayout.addWidget(Chbox)
            if move in self.checkedMoves:
                Chbox.setChecked(True)
        movelist.setLayout(movelistLayout)
        moveWidgetLayout.addWidget(movelist)
        moveWidget.setLayout(moveWidgetLayout)
        moveArea =QScrollArea()
        moveArea.setWidget(moveWidget)
        moveArea.setWidgetResizable(True)
        moveArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.itemsinroute = itemsinroute
        self.trainerinroute = trainerinroute
        
        #######
        ###### ROUTE TRACKER
        ######

        events=[]
        trainers=[]
        items=[]
        self.routelayout = QStackedLayout()
        self.routeWidget = QWidget()
        self.routedict = {}
        counter = 0
        self.currentRoute = currentRoute
        for route in self.routes:
            layout=QVBoxLayout()
            self.routedict[route] = counter
            counter+=1
            with open("routes/"+route+".json") as db:
                data = json.load(db)
                events = data["events"]
                trainers = data["trainers"]
                items = data["items"]
            floors= list(trainers.keys() | events.keys() | items.keys())
            floors.sort()
            codecounter = 0
            for floor in floors:
                if floor == "0":
                    name =QLabel("Overworld")
                else: name =QLabel(floor.upper())
                name.setMaximumSize(name.sizeHint())
                layout.addWidget(name)
                
                if floor in items and len(items[floor])>0:
                    tempname = QLabel("Items")
                    tempname.setMaximumSize(tempname.sizeHint())
                    layout.addWidget(tempname)
                    for j in items[floor]:
                        key = "ITEM-"+j
                        cbox=MyCheckbox(j,key,parent,codecounter)
                        codecounter+=1
                        if cbox.code in self.itemsinroute[route]:
                            cbox.setChecked(True)
                        cbox.stateChanged.connect(self.itemShow)
                        layout.addWidget(cbox)   
                        # ---------------------
                        #cbox.setChecked(True)
                        
                prev_name=""
                if floor in trainers and len(trainers[floor])>0:
                    tempname = QLabel("Trainers")
                    tempname.setMaximumSize(tempname.sizeHint())
                    layout.addWidget(tempname)
                    for j in trainers[floor]:
                        if j["name"]  not in skiptrainer or  prev_name != j["name"]:
                            key = "TRAINER-"+j["name"]+"_"
                            cbox=MyCheckbox(j["name"].upper(),key,parent,codecounter)
                            prev_name = j["name"]
                            layout.addWidget(cbox)
                            if cbox.code in self.trainerinroute[route]:
                                cbox.setChecked(True)
                            cbox.stateChanged.connect(self.updateTrainer)
                            
                            #cbox.setChecked(True)

                            codecounter+=1
                        mon=QWidget()
                        Flayout = FlowLayout()
                        count_level = len(j["levels"]) >1

                        for i in range(len(j["mons"])):
                            tempWidget = QWidget()
                            tempV = QVBoxLayout()
                            tempLabel = QLabel()
                            tempLabel.setPixmap(QPixmap("Sprites/mons/"+j["mons"][i].upper()+".png").scaled(64,64,Qt.KeepAspectRatio))
                            tempV.addWidget(tempLabel)
                            if count_level:
                                tempV.addWidget(QLabel(str(j["levels"][i])))
                            else :tempV.addWidget(QLabel(str(j["levels"][0])))
                            tempWidget.setLayout(tempV)
                            Flayout.addWidget(tempWidget)
                        mon.setLayout(Flayout)
                        mon.setMaximumHeight(mon.sizeHint().height())
                        layout.addWidget(mon)  

                if floor in events and len(events[floor])>0:
                    tempname = QLabel("Events")
                    tempname.setMaximumSize(tempname.sizeHint())
                    layout.addWidget(tempname)
                    for j in events[floor]:
                        key = "EVENT"+j
                        cbox=MyCheckbox(j,key,parent,codecounter)
                        if cbox.code in self.itemsinroute[route]:
                            cbox.setChecked(True)
                        codecounter+=1
                        cbox.stateChanged.connect(self.itemShow)
                        layout.addWidget(cbox)
                        #cbox.setChecked(True)

            layout.addWidget(QLabel(""))
            RouteWidget = QWidget()
            RouteWidget.setLayout(layout)
            routearea =QScrollArea()
            routearea.setWidget(RouteWidget)
            routearea.setWidgetResizable(True)
            routearea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.routelayout.addWidget(routearea)

        self.select_routes =QComboBox()
        self.select_routes.addItems(routes)
        self.select_routes.currentTextChanged.connect(self.updateroute)
        self.routeWidget.setLayout(self.routelayout)
        tempHbox = QVBoxLayout()
        tempHbox.addWidget(self.select_routes)
        tempHbox.addWidget(self.routeWidget)
        self.routeswidget = QWidget()
        self.routeswidget.setLayout(tempHbox)
        self.hSplitter = QSplitter()
        self.hSplitter.addWidget(moveArea)
        self.hSplitter.addWidget(self.routeswidget)
        self.setCentralWidget(self.hSplitter)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.parent.close()
        return super().closeEvent(a0)
    
    def updateMoves(self):
        checkbox = self.sender()
        state = checkbox.checkState()
        move= checkbox.text()
        self.parent.updateMoves(state,move)

    def updateroute(self,v):
        self.currentRoute = v
        self.parent.curr_route = v
        self.routelayout.setCurrentIndex(self.routedict[v])
    
    def itemShow(self):
        checkbox = self.sender()
        state = checkbox.checkState()
        id = checkbox.id.upper().replace(" ","")
        code = checkbox.code
        if id.startswith("ITEM-"):
            id = id.replace("ITEM-","")
            self.parent.updateItem(id,code,state,self.currentRoute)
        else :
            id = id.replace("EVENT","")
            self.parent.updateEvents(id,code,state,self.currentRoute)

    def updateTrainer(self):
        checkbox = self.sender()
        state = checkbox.checkState()
        code = checkbox.code
        self.parent.updateTrainer(state,code)