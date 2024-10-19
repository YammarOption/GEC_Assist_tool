from PyQt5 import QtGui
from PyQt5.QtWidgets import ( QSplitter,QWidget, QApplication, QMenuBar, QHBoxLayout, QGridLayout, QLabel,
                            QDesktopWidget,QGraphicsColorizeEffect, QGraphicsOpacityEffect)
from PyQt5.QtGui import QPixmap, QCloseEvent, QFont, QColor
from PyQt5.QtCore import Qt, QPoint,pyqtSignal,pyqtSlot
from QTExtra import ClickableLabel_NotSize, next_color
from GECSecWind import GECSecwindow
from qframelesswindow import FramelessMainWindow
import TwitchGECController
import os.path as op

import json

MON_PER_ROW=9 
ITEMS_PER_ROW=10 

class GECWin(FramelessMainWindow):
    twitchSignal = pyqtSignal(str,str) 

    def __init__(self):
        super(GECWin, self).__init__()


    def setup(self):
        self.setWindowTitle("GEC Tool 2.5")
        self.setWindowIcon(QtGui.QIcon('Sprites/items/surfachu.png'))
        self.MON_PER_ROW=MON_PER_ROW
        self.ITEMS_PER_ROW=ITEMS_PER_ROW
        self.twitchSignal.connect(self.twitchUpdate)
        self.curr_route=""
        if op.isfile("Data/data.json"):
            with open("Data/data.json") as savefile:
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

        self.onTop = False
        self.icons=[]
        self.itemsPic={}

        with open("routes/Summary.json") as db:
            data = json.load(db)
            self.totalMons = data["MonsNO"]
            if "Mons_per_row" in data:
                self.MON_PER_ROW=data["Mons_per_row"]  
            if "Items_per_row" in data:
                self.ITEMS_PER_ROW=data["Items_per_row"]        
            dexList = data["Monset"]
            self.totalMoves = data["ItemsNO"]
            self.totalEvents = data["MiscsNO"]
            self.TotalMoves=data["MovesNO"]
            self.totalTrainers = data["VSNO"]
            itemList = data["ItemList"]
            self.movesList = sorted(data["Moves"])
            if not self.curr_route:
                self.curr_route=data["Starting_route"]
            self.trainerinRoute[self.curr_route]=[]
            self.routes=sorted(data["Routes"])
            if len(self.checkedMons) == 0:
                self.checkedMons={i.upper():0 for i in dexList}
                self.total_checked_elements = {}
                for i in itemList:
                    item =list(i.keys())[0]
                    if not item == "blank" :
                        #Couple with #current item and #max item
                        self.total_checked_elements[item.replace(" ","").upper()]=[0,i[item][1]]
                for i in self.routes:
                    self.checked_elements_per_route[i] = []
                    self.trainerinRoute[i]=[]
        self.dexlayout=QGridLayout()
        self.itemlayout =QGridLayout()
        self.movescout=0
        ###############################################
        ## DEX
        ############################################### 
        count=0
        self.dexPics={}
        for img in dexList:
            img=img.upper()
            if img == "VUOTO":
                pic=QLabel()
                image=QPixmap("Sprites/items/blank.png")
                pic.setPixmap(image)     
                self.dexlayout.addWidget(pic,int(count/self.MON_PER_ROW), count%self.MON_PER_ROW)                  
                count=count+1
                continue
            pic=ClickableLabel_NotSize("DEX"+img,self,self.checkedMons[img])
            self.dexPics[img.upper()]=pic
            image=QPixmap("Sprites/mons/"+img+".png",)
            pic.setPixmap(image)
            self.icons.append(pic)
            pic.setGraphicsEffect(next_color(self.checkedMons[img]))
            self.dexlayout.addWidget(pic,int(count/self.MON_PER_ROW), count%self.MON_PER_ROW)
            count=count+1
        self.dexWidget=QWidget()
        self.dexWidget.setLayout(self.dexlayout)
        self.dexWidget.setStyleSheet('QWidget{background-color: white}')
        
        ###############################################
        ## TRANSPARENT HOLE
        ###############################################
        self.windowWidget = QLabel()
        self.windowWidget.setFocusPolicy(Qt.NoFocus)
        self.windowWidget.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.windowWidget.setAttribute(Qt.WA_TranslucentBackground, True)

        ################################################
        ## SUMMARY WINDOW (TOP)
        ############################################## 
        # Reading the data
        self.deximage = ClickableLabel_NotSize('dexCount')
        self.deximage.setPixmap(QPixmap("Sprites/ball.png"))
        self.deximage.setScaledContents(False)
        self.itemImage=ClickableLabel_NotSize('itemsCount')
        self.itemImage.setPixmap(QPixmap("Sprites/strum.png"))
        self.itemImage.setScaledContents(False)
        self.trainerImage=ClickableLabel_NotSize('TrainersCount')
        self.trainerImage.setPixmap(QPixmap("Sprites/VS_Seeker.png"))
        self.trainerImage.setScaledContents(False)
        self.moveImage=ClickableLabel_NotSize('movesCount')
        self.moveImage.setPixmap(QPixmap("Sprites/moves.png"))
        self.moveImage.setScaledContents(False)
        self.miscImage=ClickableLabel_NotSize('MiscCount')
        self.miscImage.setPixmap(QPixmap("Sprites/Ribbon.png"))
        self.miscImage.setScaledContents(False)
        self.img_row = [self.deximage,self.itemImage,self.trainerImage,self.moveImage,self.miscImage]
        self.counter_row = [
            QLabel(str(self.totalMons)+"/"+str(self.totalMons)),
            QLabel(str(self.totalMoves)+"/"+str(self.totalMoves)),
            QLabel(str(self.totalTrainers)+"/"+str(self.totalTrainers)),
            QLabel(str(self.TotalMoves)+"/"+str(self.TotalMoves)),
            QLabel(str(self.totalEvents)+"/"+str(self.totalEvents))
        ]
        tmpA=[
            str(self.dex_counter)+"/"+str(self.totalMons),
            str(self.items_counter)+"/"+str(self.totalMoves),
            str(self.trainer_counter)+"/"+str(self.totalTrainers),
            str(self.moves_counter)+"/"+str(self.TotalMoves),
            str(self.event_counter)+"/"+str(self.totalEvents)]
        # Filling the grid
        topgrid = QHBoxLayout()
        #topgrid.addWidget(QLabel(""),stretch=0)
        for i in range(0,5):
            box=QHBoxLayout()
            tempwidget=QWidget()
            box.addWidget(self.img_row[i],alignment=Qt.AlignRight)
            box.addWidget(self.counter_row[i],alignment=Qt.AlignLeft)
            self.counter_row[i].setFont(QFont("Sanserif", 12))
            self.counter_row[i].setMinimumSize(self.counter_row[i].maximumSize())
            tempwidget.setLayout(box)
            topgrid.addWidget(tempwidget)

        #topgrid.addWidget(QLabel(""),stretch=0)
        
        self.topwdidget = QWidget()
        self.topwdidget.setLayout(topgrid)
        #self.topwdidget.setMinimumWidth(topgrid.totalMinimumSize().width()) 
        self.topwdidget.setMaximumHeight(topgrid.totalMinimumSize().height()) 

        for i in range(0,5):
            self.counter_row[i].setText(tmpA[i])
        self.topwdidget.setStyleSheet("background-color: white")
        ################################################
        ## Vertical splitter
        ##############################################
        self.vSplitter = QSplitter(Qt.Vertical)
        self.vSplitter.addWidget(self.topwdidget)
        #self.vSplitter.addWidget(self.windowhole)
        self.vSplitter.setStretchFactor(0,1)
        self.vSplitter.setStretchFactor(1,1)

        ###############################################
        ## ITEM LIST
        ############################################### 
        count=0
        for couple in itemList:
            item =list(couple.keys())[0]
            if item == "blank":
                pic=QLabel()
                image=QPixmap("Sprites/items/blank.png")
                pic.setPixmap(image)     
                self.itemlayout.addWidget(pic,int(count/self.ITEMS_PER_ROW), count%self.ITEMS_PER_ROW)                  
                count=count+1
                continue
            pic=ClickableLabel_NotSize("ITEM"+item)
            image=QPixmap("Sprites/items/"+itemList[count][item][0])
            self.itemsPic[item.replace(" ","").upper()] = pic
            pic.setPixmap(image)
            if item.startswith("PKRS_") and \
                self.total_checked_elements[item.replace(" ","").upper()][0] < self.total_checked_elements[item.replace(" ","").upper()][1]:
                color_effect = QGraphicsOpacityEffect() 
                # setting opacity level 
                color_effect.setOpacity(0) 
                # adding opacity effect to the label 
                pic.setGraphicsEffect(color_effect) 
            else:
                label = QLabel(str(self.total_checked_elements[item.replace(" ","").upper()][0]),parent=self.itemsPic[item.replace(" ","").upper()])
                label.setStyleSheet("background-color: rgba(0,0,0,0%)")
                label.setFont(QFont("Sanserif", 7,QFont.Bold))
                #REMOVE COLOR IF NOT GET YET
                if self.total_checked_elements[item.replace(" ","").upper()][0] < self.total_checked_elements[item.replace(" ","").upper()][1]:
                    color_effect = QGraphicsColorizeEffect() 
                    # setting opacity level 
                    color_effect.setColor(QColor(0,0,0)) 
                    pic.setGraphicsEffect(color_effect) 
                # MORE THAN ONE  OBTAINED: SHOW LABLE
                if self.total_checked_elements[item.replace(" ","").upper()][0] >self.total_checked_elements[item.replace(" ","").upper()][1]: 
                    label.show()
                else: label.hide() #EXACTLY ONE OBTAINED: ONLY COLOR, NO LABEL

            self.itemlayout.addWidget(pic,int(count/self.ITEMS_PER_ROW), count%self.ITEMS_PER_ROW)            
            count=count+1
        self.itemwidget=QWidget()
        self.itemwidget.setLayout(self.itemlayout)
        self.itemwidget.setStyleSheet('QWidget{background-color: white}')

        ################################################
        ## HORIZONTAL SPLITTER
        ##############################################
        self.hSplitter = QSplitter()
        self.hSplitter.addWidget(self.itemwidget)
        self.hSplitter.addWidget(self.vSplitter)
        self.hSplitter.addWidget(self.dexWidget)
        self.hSplitter.setStretchFactor(0,1)
        self.hSplitter.setStretchFactor(1,25)
        self.hSplitter.setStretchFactor(2,1)
    
        ################################################
        ## MAIN WINDOW
        ##############################################
        self.setAttribute(Qt.WA_TranslucentBackground)

        menuBar = QMenuBar(self.titleBar)
        menuBar.addAction('Chiudi',self.quit)
        menuBar.addAction('Blocca/Sblocca',self.changeflags)
        self.titleBar.layout().insertStretch(1, 1)
        self.titleBar.layout().insertWidget(1, menuBar, 10, Qt.AlignRight)
        self.setMenuWidget(menuBar)
        self.statusBar().setStyleSheet("background-color: white")
        self.setCentralWidget(self.hSplitter)

        #### SECONDARY WINDOW
        self.extraWindow = GECSecwindow(self,self.movesList,self.checkedMoves, self.routes,self.curr_route, self.checked_elements_per_route,self.trainerinRoute)
        self.extraWindow.updateroute(self.curr_route)
        self.extraWindow.select_routes.setCurrentText(self.curr_route)
        self.extraWindow.colorAllCombobox()

        if (op.isfile("Data/TwitchConfig.json")):
            self.TwitchController=TwitchGECController.TwitchGECController(self.twitchSignal,"Data/TwitchConfig.json")
            self.TwitchController.start()

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
        with open("Data/data.json",'w') as savefile:
            json.dump(fp=savefile,indent=4,obj=save,default=list)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.save()
        self.extraWindow.close()
        if op.isfile("Data/TwitchConfig.json"):
            self.TwitchController.quit()
        return super().closeEvent(a0)

    def quit(self):
        self.extraWindow.close()
        self.close()
        exit()
            
    def changeflags(self):
        if self.onTop:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.onTop = False
        else:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            self.onTop = True
        self.show()

    def updateMoves(self,state,move):
        if state:
            self.moves_counter += 1
            self.checkedMoves.append(move)
            self.counter_row[3].setText(str(self.moves_counter)+"/"+str(self.TotalMoves))
        else :
            self.moves_counter -= 1
            self.checkedMoves.remove(move)
            self.counter_row[3].setText(str(self.moves_counter)+"/"+str(self.TotalMoves))

    def twitchUpdateMove(self,move,state):
        moves = move.split(",")
        for m in moves:
            if m.upper() not in (name.upper().replace(" ","") for name in self.movesList): continue
            if state and m not in self.checkedMoves:
                self.moves_counter += 1
                self.checkedMoves.append(m)
                self.counter_row[3].setText(str(self.moves_counter)+"/"+str(self.TotalMoves))
            elif not state and m in self.checkedMoves:
                self.moves_counter -= 1
                self.checkedMoves.remove(m)
                self.counter_row[3].setText(str(self.moves_counter)+"/"+str(self.TotalMoves))
            self.extraWindow.twitchUpdateMoves(m,state)

    def twitchUpdateTrainer(self,name,state):
        code=self.extraWindow.twitchUpdateTrainers(name,state)
        if code == "": return
        if state:
            self.trainer_counter += 1
            self.trainerinRoute[self.curr_route].append(code)
            self.counter_row[2].setText(str(self.trainer_counter)+"/"+str(self.totalTrainers))
        else :
            self.trainer_counter -= 1
            self.trainerinRoute[self.curr_route].remove(code)
            self.counter_row[2].setText(str(self.trainer_counter)+"/"+str(self.totalTrainers))

    def updateTrainer(self,state,code):
        if state:
            self.trainer_counter += 1
            self.trainerinRoute[self.curr_route].append(code)
            self.counter_row[2].setText(str(self.trainer_counter)+"/"+str(self.totalTrainers))
        else :
            self.trainer_counter -= 1
            self.trainerinRoute[self.curr_route].remove(code)
            self.counter_row[2].setText(str(self.trainer_counter)+"/"+str(self.totalTrainers))
        self.counter_row[2].adjustSize()

    def updateMons(self,id,color):
        id = id.replace("DEX","")
        if color == 1 and not (self.checkedMons[id]==1):
            self.dex_counter+=1
        elif not (color == 1) and self.checkedMons[id]==1: self.dex_counter=max(self.dex_counter-1,0)
        if id.startswith("UNOWN") and color > 0:
            self.updateEvents("26UNOWN","",color==1,self.curr_route)
        elif (color == 1) ^ (self.checkedMons[id]==1) and \
            (id=="ENTEI" or id=="RAIKOU" or id=="SUICUNE"
            or id =="SUDOWOODO" or id =="LAPRAS" or id =="SNORLAX"
            or id =="LUGIA" or id =="HO-OH" or id =="MEW" or id =="CELEBI"):
            self.updateEvents(id,"",color==1,self.curr_route)
        self.counter_row[0].setText(str(self.dex_counter)+"/"+str(self.totalMons))
        self.checkedMons[id]=color

    def twitchUpdateMons(self,id,update):
        ids = id.split(",")
        for i in ids:     
            if i in self.dexPics:
                self.dexPics[i].twitchUpdate(update)
                self.updateMons(i,update)

    def updateItem(self,id,idNumb,state,route):
        if id.startswith("GETTONI"):
            id = "GETTONI"
        if id.startswith("MAMMA-"):
            self.updateItem(id.replace("MAMMA-",""),idNumb,state,route)
            id = "STRUMENTIMAMMA"
        if id.startswith("DECO-"):
            id = "DECORAZONI"
        id = id.replace(" ","").upper().replace("(N)","").replace("($)","")
        ## CASE 1: OLD ITEM/EVENT 
        try :
            if state:  ## NEW CHECK: UPDATE COUNTERS, eventually show label
                self.items_counter+=1
                self.total_checked_elements[id][0]+=1
                self.checked_elements_per_route[route].append(idNumb)
                ## Update label
                if id.startswith("PKRS_") and self.total_checked_elements[id][0] == self.total_checked_elements[id][1]:
                    color_effect = QGraphicsOpacityEffect() 
                    # setting opacity level 
                    color_effect.setOpacity(100) 
                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect)
                elif self.total_checked_elements[id][0] == self.total_checked_elements[id][1]:
                    color_effect = QGraphicsColorizeEffect() 
                    color_effect.setStrength(0) 
                    self.itemsPic[id].setGraphicsEffect(color_effect) 
                elif  self.total_checked_elements[id][0] > self.total_checked_elements[id][1]:
                    label = self.itemsPic[id].findChild(QLabel)
                    label.setText(str(self.total_checked_elements[id][0]))
                    label.adjustSize() 
                    label.show()

            else: ## CHECK REMOVED: REDUCE COUNTER, EVENTUALLY REMOVE LABEL
                self.items_counter-=1
                self.total_checked_elements[id][0]-=1
                
                self.checked_elements_per_route[route].remove(idNumb)
                label = self.itemsPic[id].findChild(QLabel)
                if id.startswith("PKRS_") and self.total_checked_elements[id][0] < self.total_checked_elements[id][1]:
                    color_effect = QGraphicsOpacityEffect() 
                    # setting opacity level 
                    color_effect.setOpacity(0) 
                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect)
                elif self.total_checked_elements[id][0] > self.total_checked_elements[id][1]:#Reduce LABEL, remove counter
                    label.setText(str(self.total_checked_elements[id][0]))
                elif self.total_checked_elements[id][0] == self.total_checked_elements[id][1]:
                    label.hide()
                elif self.total_checked_elements[id][0] < self.total_checked_elements[id][1]:#FADE LABEL, remove counter
                        color_effect = QGraphicsColorizeEffect() 
                        # setting opacity level 
                        color_effect.setColor(QColor(0,0,0)) 
                        # adding opacity effect to the label 
                        self.itemsPic[id].setGraphicsEffect(color_effect) 
        except Exception as err:
            print("Exc "+str(err))
        self.counter_row[1].setText(str(self.items_counter)+"/"+str(self.totalMoves))
        self.counter_row[1].adjustSize()
    
    
    def updateEvents(self,id,idNumb,state,route):
        updatelabel=True
        ## CASE 1: OLD ITEM/EVENT 
        id = id.replace(" ","").upper()
        if id.startswith("TRAPPOLA"):
            id = "POK\u00c9MONTRAPPOLA"
        if id.startswith("PUZZLE"):
            id = "PUZZLEROVINE"
        if id.startswith("NUMEROTELEFONO"):
            id = "NUMERIDITELEFONO"
        if id.startswith("FRATELLISETTIMANA"):
            id = "FRATELLISETTIMANA"
        if id.startswith("MESSAGGIO"):
            id = "MESSAGGIALPC"
        try :
            if state:  ## NEW CHECK: UPDATE COUNTERS, eventually show label
                self.event_counter+=1
                self.total_checked_elements[id][0]+=1
                if idNumb:
                    self.checked_elements_per_route[route].append(idNumb)
                ## Update label
                if id.startswith("PKRS_") and self.total_checked_elements[id][0] == self.total_checked_elements[id][1]:
                    color_effect = QGraphicsOpacityEffect() 
                    # setting opacity level 
                    color_effect.setOpacity(100) 
                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect)
                elif id == "26UNOWN" and self.total_checked_elements[id][0] < self.total_checked_elements[id][1]:
                    self.event_counter-=1
                    updatelabel=False
                elif self.total_checked_elements[id][0] == self.total_checked_elements[id][1] and id:
                    color_effect = QGraphicsColorizeEffect() 
                    color_effect.setStrength(0) 
                    self.itemsPic[id].setGraphicsEffect(color_effect) 
                elif  self.total_checked_elements[id][0] > self.total_checked_elements[id][1]:
                    label = self.itemsPic[id].findChild(QLabel)
                    label.setText(str(self.total_checked_elements[id][0]))
                    label.adjustSize() 
                    label.show()

            else: ## CHECK REMOVED: REDUCE COUNTER, EVENTUALLY REMOVE LABEL
                self.event_counter-=1
                self.total_checked_elements[id][0]-=1
                if idNumb:
                    self.checked_elements_per_route[route].remove(idNumb)
                label = self.itemsPic[id].findChild(QLabel)
                if id.startswith("PKRS_") and self.total_checked_elements[id][0] < self.total_checked_elements[id][1]:
                    color_effect = QGraphicsOpacityEffect() 
                    # setting opacity level 
                    color_effect.setOpacity(0) 
                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect)
                elif self.total_checked_elements[id][0] > self.total_checked_elements[id][1]:#Reduce LABEL, remove counterù
                    label.setText(str(self.total_checked_elements[id][0]))
                elif self.total_checked_elements[id][0] == self.total_checked_elements[id][1]:
                    label.hide()
                elif id == "26UNOWN" and self.total_checked_elements[id][0] < self.total_checked_elements[id][1]-1:
                    self.event_counter+=1
                    updatelabel=False
                elif self.total_checked_elements[id][0] < self.total_checked_elements[id][1]:#FADE LABEL, remove counter
                        color_effect = QGraphicsColorizeEffect() 
                        # setting opacity level 
                        color_effect.setColor(QColor(0,0,0)) 
                        # adding opacity effect to the label 
                        self.itemsPic[id].setGraphicsEffect(color_effect) 
        except Exception as err:
            print("Exc: "+str(err))
        if updatelabel:
            self.counter_row[4].setText(str(self.event_counter)+"/"+str(self.totalEvents))
            self.counter_row[4].adjustSize()

    def twitchUpdateCollectibles(self,name,state,prefix):
            id,idNumb,route=self.extraWindow.twitchUpdateCollectibles(name,state,prefix)
            if not id: return
            if prefix == "ITEM-":
                self.updateItem(id,idNumb,state,route)
                self.counter_row[1].adjustSize()
            else:
                self.updateEvents(id,idNumb,state,route)
                self.counter_row[4].adjustSize()

    @pyqtSlot(str,str)
    def twitchUpdate( self, type, text ):
        if type == "MON":
            self.twitchUpdateMons(text.split("@")[0],int(text.split("@")[1]))
        if type == "TR":
            self.twitchUpdateTrainer(text.split("@")[0],text.split("@")[1]=="1")
        if type == "ITEM-" or type=="EVENT":
            self.twitchUpdateCollectibles(text.split("@")[0],text.split("@")[1]=="1",type)
        if type == "MOVE":
            self.twitchUpdateMove(text.split("@")[0],text.split("@")[1]=="1")
        if type == "SAVE":
            self.save()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
   
app = QApplication([])
window = GECWin()
window.setup()
window.show()
window.extraWindow.show()
app.exec()

