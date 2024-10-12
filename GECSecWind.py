from PyQt5.QtWidgets import (QGridLayout,QWidget,QVBoxLayout, QStackedLayout, QMainWindow, QScrollArea, 
                            QLabel, QCheckBox, QSplitter, QComboBox)
from PyQt5.QtGui import  QPixmap, QCloseEvent, QFont
from PyQt5.QtCore import Qt
from QTExtra import FlowLayout,MyCheckbox 
from PyQt5 import QtGui
import json

skiptrainer=["Rivale","Rivale Opzionale","???"]

class GECSecwindow(QMainWindow):
    def __init__(self,parent,moves,checkedmoves,routes,currentRoute,itemsinroute,trainerinroute):
        super(GECSecwindow, self).__init__()
        self.setWindowTitle("GEC Tool 2.5 Route Tracker")
        self.parent = parent
        self.setWindowIcon(self.parent.windowIcon())
        self.moves = moves
        self.movesboxes={}
        self.itemboxes={}
        self.trainerboxes={}
        self.totalcheck={}
        self.currentCheck={}
        self.checkedMoves = checkedmoves
        self.routes = routes
        #######
        ###### MOVES LISTBOX
        ######
        moveWidget = QWidget()
        moveWidgetLayout = QVBoxLayout()
        moveheader = QLabel("MOSSE")
        moveheader.setFont(QFont("Sanserif", 10))
        moveWidgetLayout.addWidget(moveheader)
        movelist=QWidget()
        checkedMovelist=QWidget()
        movelistLayout=QGridLayout()
        checkedMovelistLayout=QGridLayout()
        counter = 0
        for move in moves:  
            Chbox = QCheckBox(move)
            Chbox.stateChanged.connect(self.updateMoves)
            Chbox2 = QCheckBox(move)
            Chbox2.stateChanged.connect(self.updateMoves)
            Chbox2.blockSignals(True)
            Chbox2.setChecked(True)
            Chbox2.blockSignals(False)
            self.movesboxes[move.upper().replace(" ","")] = (Chbox,Chbox2)
            if move in self.checkedMoves:
                Chbox.hide()
                Chbox.sister=Chbox2
                Chbox2.sister = Chbox 
            else : Chbox2.hide()
            movelistLayout.addWidget(Chbox,int(counter%int((len(moves)/3))+1),int(counter/(len(moves)/3)))
            checkedMovelistLayout.addWidget(Chbox2,int(counter%int((len(moves)/3))+1),int(counter/(len(moves)/3)))
            Chbox2.setStyleSheet("background-color:rgba(51, 218, 74, 0.84)")
            Chbox.setStyleSheet("background-color: rgba(250, 150, 150, 0.8)")
            Chbox.setFont(QFont("Sanserif", 7,QFont.Bold))
            Chbox2.setFont(QFont("Sanserif", 7,QFont.Bold))
            counter+=1
        movelist.setLayout(movelistLayout)
        checkedMovelist.setLayout(checkedMovelistLayout)
        moveWidgetLayout.addWidget(movelist)
        moveWidgetLayout.addWidget(checkedMovelist)
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
            self.trainerboxes[route.upper()]={}
            self.itemboxes[route.upper()]={}
            self.totalcheck[route.upper()]=0
            self.currentCheck[route.upper()]=0
            layout=QVBoxLayout()
            self.routedict[route] = counter
            counter+=1
            with open("routes/"+route+".json") as db:
                data = json.load(db)
                print(route)
                events = data["events"]
                trainers = data["trainers"]
                items = data["items"]
            floors= list(trainers.keys() | events.keys() | items.keys())
            floors.sort()
            codecounter = 0
            for floor in floors:
                self.trainerboxes[route.upper()][floor.upper()]={}
                self.itemboxes[route.upper()][floor.upper()]={}
                if floor == "0":
                    name =QLabel("Overworld")
                elif floor == "Piano 0":
                    name = QLabel("Piano Terra")
                else: name =QLabel(floor.upper())
                name.setFont(QFont("Sanserif", 15))
                name.setMaximumSize(name.sizeHint())
                layout.addWidget(name)
                if floor in items and len(items[floor])>0:
                    tempname = QLabel("Oggetti")
                    tempname.setFont(QFont("Sanserif", 10))
                    tempname.setMaximumSize(tempname.sizeHint())
                    layout.addWidget(tempname)
                    for j in items[floor]:
                        key = "ITEM-"+j
                        cbox=MyCheckbox(j.replace("PKRS_","").replace("MAMMA-","").replace("DECO-",""),key,parent,codecounter)
                        codecounter+=1
                        if cbox.code in self.itemsinroute[route]:
                            cbox.blockSignals(True)
                            cbox.setChecked(True)
                            cbox.blockSignals(False)
                            self.currentCheck[route.upper()]+=1
                        cbox.stateChanged.connect(self.itemShow)
                        layout.addWidget(cbox)   
                        self.itemboxes[route.upper()][floor.upper()][cbox.code]=cbox
                        self.totalcheck[route.upper()]+=1


                        #--------------------------------------------------
                        #cbox.setChecked(True)
                        #--------------------------------------------------
                        
                prev_name=""
                if floor in trainers and len(trainers[floor])>0:
                    tempname = QLabel("Allenatori")
                    tempname.setFont(QFont("Sanserif", 10))
                    tempname.setMaximumSize(tempname.sizeHint())
                    layout.addWidget(tempname)
                    for j in trainers[floor]:
                        if j["name"]  not in skiptrainer or  prev_name != j["name"]:
                            key = "TRAINER-"+j["name"]+"_"
                            cbox=MyCheckbox(j["name"].upper(),key,parent,codecounter)
                            prev_name = j["name"]
                            layout.addWidget(cbox)
                            if cbox.code in self.trainerinroute[route]:
                                cbox.blockSignals(True)
                                cbox.setChecked(True)
                                cbox.blockSignals(False)
                                self.currentCheck[route.upper()]+=1
                            cbox.stateChanged.connect(self.updateTrainer)
                            self.trainerboxes[route.upper()][floor.upper()][cbox.code]=cbox
                            self.totalcheck[route.upper()]+=1

                            #--------------------------------------------------
                            #cbox.setChecked(True)
                            #--------------------------------------------------

                            codecounter+=1
                        mon=QWidget()
                        Flayout = FlowLayout()
                        count_level = len(j["levels"]) >1

                        for i in range(len(j["mons"])):
                            tempWidget = QWidget()
                            tempV = QVBoxLayout()
                            tempLabel = QLabel()
                            tempLabel.setPixmap(QPixmap("Sprites/mons/"+j["mons"][i].upper()+".png"))
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
                    tempname = QLabel("Eventi")
                    tempname.setFont(QFont("Sanserif", 10))
                    tempname.setMaximumSize(tempname.sizeHint())
                    layout.addWidget(tempname)
                    for j in events[floor]:
                        key = "EVENT"+j
                        cbox=MyCheckbox(j,key,parent,codecounter)
                        if cbox.code in self.itemsinroute[route]:
                            cbox.blockSignals(True)
                            cbox.setChecked(True)
                            cbox.blockSignals(False)
                            self.currentCheck[route.upper()]+=1
                        codecounter+=1
                        cbox.stateChanged.connect(self.itemShow)
                        layout.addWidget(cbox)
                        self.itemboxes[route.upper()][floor.upper()][cbox.code]=cbox
                        self.totalcheck[route.upper()]+=1

                        #--------------------------------------------------
                        #cbox.setChecked(True)
                        #--------------------------------------------------
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

    def colorAllCombobox(self):
        for i in range(self.select_routes.count()):
            self.colorCombobox(i)

    def colorCombobox(self,index):
        route = self.select_routes.itemText(index).upper()
        if self.currentCheck[route] == self.totalcheck[route]:
            self.select_routes.model().item(index).setForeground(QtGui.QColor("green"))
        else: self.select_routes.model().item(index).setForeground(QtGui.QColor("black"))


    def closeEvent(self, a0: QCloseEvent) -> None:
        self.parent.close()
        return super().closeEvent(a0)
        
    def updateMoves(self):
        checkbox = self.sender()
        state = checkbox.checkState()
        move= checkbox.text().upper().replace(" ","")
        cbox1= self.movesboxes[move][0]
        cbox2= self.movesboxes[move][1]
        cbox1.blockSignals(True)
        cbox2.blockSignals(True)
        cbox1.setChecked(state)
        cbox2.setChecked(state)
        cbox1.blockSignals(False)
        cbox2.blockSignals(False)
        if state:
            cbox1.hide()
            cbox2.show()
        else : 
            cbox1.show()
            cbox2.hide()
        self.parent.updateMoves(state,move)

    def twitchUpdateMoves(self,move,state):
        cbox1= self.movesboxes[move][0]
        cbox2= self.movesboxes[move][1]
        cbox1.blockSignals(True)
        cbox2.blockSignals(True)
        cbox1.setChecked(state)
        cbox2.setChecked(state)
        cbox1.blockSignals(False)
        cbox2.blockSignals(False)
        if state:
            cbox1.hide()
            cbox2.show()
        else : 
            cbox1.show()
            cbox2.hide()


    def updateroute(self,v):
        self.currentRoute = v
        self.parent.curr_route = v
        self.routelayout.setCurrentIndex(self.routedict[v])
    
    def itemShow(self):
        checkbox = self.sender()
        state = checkbox.checkState()
        id = checkbox.id.upper().replace(" ","")
        code = checkbox.code
        if state:
            self.currentCheck[self.currentRoute.upper()]+=1
        else: self.currentCheck[self.currentRoute.upper()]-=1
        self.colorCombobox(self.select_routes.currentIndex())
        if id.startswith("ITEM-"):
            id = id.replace("ITEM-","")
            self.parent.updateItem(id,code,state,self.currentRoute)
        else :
            id = id.replace("EVENT","")
            self.parent.updateEvents(id,code,state,self.currentRoute)

    def twitchUpdateCollectibles(self,name,state,prefix):
        sep=name.split("->")
        if len(sep) < 2:
            return "","",""
        floor =sep[0].replace(" ","") 
        key =prefix+ sep[1].replace(" ","")
        print(key)
        searchKey=""
        #find first match for checkbox  given floor and route
        if floor not in self.itemboxes[self.currentRoute.upper()]: return ""
        for name in self.itemboxes[self.currentRoute.upper()][floor.upper()]:
            if key in name:
                searchKey=name
                print(searchKey)
                if (state and not self.itemboxes[self.currentRoute.upper()][floor.upper()][searchKey].checkState()) or \
                    (not state and self.itemboxes[self.currentRoute.upper()][floor.upper()][searchKey].checkState()):
                    break
                else: searchKey=""
        if searchKey:
            box=self.itemboxes[self.currentRoute.upper()][floor.upper()][searchKey]
            if not state == box.isChecked():
                if state:
                    self.currentCheck[self.currentRoute.upper()]+=1
                else: self.currentCheck[self.currentRoute.upper()]-=1
                self.colorCombobox(self.select_routes.currentIndex())
                #update color


            box.blockSignals(True)
            box.setChecked(state)
            box.blockSignals(False)
            return box.id.upper().replace(" ","").replace(prefix,""), box.code, self.currentRoute
        return "","",""

    def updateTrainer(self):
        checkbox = self.sender()
        state = checkbox.checkState()
        code = checkbox.code
        if state:
            self.currentCheck[self.currentRoute.upper()]+=1
        else: self.currentCheck[self.currentRoute.upper()]-=1
        self.colorCombobox(self.select_routes.currentIndex())
        self.parent.updateTrainer(state,code)

    def twitchUpdateTrainers(self,name,state):
        sep=name.split("->")
        if len(sep) < 2:
            return ""
        floor =sep[0].replace(" ","") 
        key ="TRAINER-"+ sep[1].replace(" ","").upper()
        searchKey=""
        #find first match for checkbox  given floor and route
        if floor not in self.trainerboxes[self.currentRoute.upper()]: return ""
        for trainername in self.trainerboxes[self.currentRoute.upper()][floor.upper()]:
            if key in trainername:
                searchKey=trainername
                if (state and not self.trainerboxes[self.currentRoute.upper()][floor.upper()][searchKey].checkState()) or \
                    (not state and self.trainerboxes[self.currentRoute.upper()][floor.upper()][searchKey].checkState()):
                    break
                else: searchKey=""
        if searchKey:
            box = self.trainerboxes[self.currentRoute.upper()][floor.upper()][searchKey]
            if not state == box.isChecked():
                if state:
                    self.currentCheck[self.currentRoute.upper()]+=1
                else: self.currentCheck[self.currentRoute.upper()]-=1
                #update
            box.blockSignals(True)
            box.setChecked(state)
            box.blockSignals(False)
        return searchKey