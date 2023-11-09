from PyQt5 import QtGui
from PyQt5.QtWidgets import ( QSplitter,QWidget, QApplication, QMenuBar, 
                            QScrollArea, QHBoxLayout, QGraphicsColorizeEffect, QLabel,
                            QDesktopWidget,QGraphicsOpacityEffect)
from PyQt5.QtGui import QPixmap, QCloseEvent, QFont,QColor
from PyQt5.QtCore import Qt, QPoint
from QTExtra import FlowLayout, ClickableLabel_NotSize, next_color
from GECSecWind import GECSecwindow
from qframelesswindow import FramelessMainWindow
import os.path as op

import json


class GECWin(FramelessMainWindow):
    def __init__(self):
        super(GECWin, self).__init__()
        self.setWindowTitle("GEC Tool 2.5")
        self.setWindowIcon(QtGui.QIcon('Sprites/items/DEX.png'))

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
            self.curr_route="Biancavilla"
            self.checked_elements_per_route={}
            self.trainerinRoute={}
            self.trainerinRoute[self.curr_route]=[]
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
            dexList = data["Monset"]
            self.totalMoves = data["ItemsNO"]
            self.totalEvents = data["MiscsNO"]
            self.TotalMoves=data["MovesNO"]
            self.totalTrainers = data["VSNO"]
            itemList = data["ItemList"]
            self.movesList = sorted(data["Moves"])
            self.routes=sorted(data["Routes"])
            if len(self.checkedMons) == 0:
                self.checkedMons={i:0 for i in dexList}
                self.total_checked_elements = {}
                for i in itemList:
                    item =list(i.keys())[0]
                    if not item == "blank" :
                        self.total_checked_elements[item.replace(" ","").upper()]=0
                for i in self.routes:
                    self.checked_elements_per_route[i] = []
                    self.trainerinRoute[i]=[]
        self.dexlayout=FlowLayout()
        self.itemlayout = FlowLayout()
        self.movescout=0
        ###############################################
        ## DEX
        ###############################################
        count=0
        for img in dexList:
            if img == 'blank':
                continue
            pic=ClickableLabel_NotSize("DEX"+img,self,self.checkedMons[img])
            image=QPixmap("Sprites/mons/"+img.upper()+".png",)#.scaled(64,64,Qt.KeepAspectRatio)
            pic.setPixmap(image)
            self.icons.append(pic)
            pic.setGraphicsEffect(next_color(self.checkedMons[img]))
            self.dexlayout.addWidget(pic)
        
        tempW = QWidget()
        tempW.setLayout(self.dexlayout)
        self.dexWidget=QScrollArea()
        self.dexWidget.setWidget(tempW)
        self.dexWidget.setStyleSheet('QWidget{background-color: white}')
        self.dexWidget.setWidgetResizable(True)
        self.dexWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
       
        
        ###############################################
        ## TRANSPARENT HOLE
        ###############################################
        self.windowWidget = QLabel()
        self.windowWidget.setFocusPolicy(Qt.NoFocus)
        self.windowWidget.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.windowWidget.setAttribute(Qt.WA_TranslucentBackground, True)

        ###############################################
        ## ITEM LIST
        ############################################### 

        count=0
        for couple in itemList:
            item =list(couple.keys())[0]
            if item == "blank":
                count=count+1
                continue
            pic=ClickableLabel_NotSize("ITEM"+item)
            image=QPixmap("Sprites/items/"+itemList[count][item][0])
            self.itemsPic[item.replace(" ","").upper()] = pic
            pic.setPixmap(image)
            if (self.total_checked_elements[item.replace(" ","").upper()] < 1 and not item == "GETTONI") or (item  == "GETTONI" and self.total_checked_elements[item.replace(" ","").upper()] <14):
                color_effect = QGraphicsColorizeEffect() 
                # setting opacity level 
                color_effect.setColor(QColor(0,0,0)) 

                # adding opacity effect to the label 
                pic.setGraphicsEffect(color_effect) 
            elif  not item == "GETTONI" and self.total_checked_elements[item.replace(" ","").upper()] >1:
                label = QLabel(str(self.total_checked_elements[item.replace(" ","").upper()]),parent=self.itemsPic[item.replace(" ","").upper()])
                label.setStyleSheet("background-color: rgba(0,0,0,0%)")
                label.setFont(QFont("Sanserif", 7,QFont.Bold))
                label.show()
            ## Add eventual label
            self.itemlayout.addWidget(pic)            
            count=count+1
        
        mainItem = QWidget()
        mainItem.setLayout(self.itemlayout)
        self.itemwidget=QScrollArea()
        self.itemwidget.setWidget(mainItem)
        self.itemwidget.setStyleSheet('QWidget{background-color: white}')
        self.itemwidget.setWidgetResizable(True)
        self.itemwidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)        

        ################################################
        ## HORIZONTAL SPLITTER
        ##############################################
        self.hSplitter = QSplitter()
        self.hSplitter.addWidget(self.itemwidget)
        self.hSplitter.addWidget(self.windowWidget)
        self.hSplitter.addWidget(self.dexWidget)
        self.hSplitter.setStretchFactor(0,1)
        self.hSplitter.setStretchFactor(1,25)
        self.hSplitter.setStretchFactor(2,1)
       

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
        topgrid.addWidget(QLabel(""))
        for i in range(0,5):
            box=QHBoxLayout()
            tempwidget=QWidget()
            box.addWidget(self.img_row[i],alignment=Qt.AlignRight)
            box.addWidget(self.counter_row[i],alignment=Qt.AlignLeft)
            self.counter_row[i].setFont(QFont("Sanserif", 15))
            self.counter_row[i].setMinimumSize(self.counter_row[i].maximumSize())
            tempwidget.setLayout(box)
            topgrid.addWidget(tempwidget,stretch=2)
        topgrid.addWidget(QLabel(""),stretch=0)
        
        self.topwdidget = QWidget()
        self.topwdidget.setLayout(topgrid)
        self.topwdidget.setMinimumWidth(topgrid.totalMinimumSize().width()) 
        for i in range(0,5):
            self.counter_row[i].setText(tmpA[i])

        self.topwdidget.setStyleSheet("background-color: white")
        ################################################
        ## Vertical splitter
        ##############################################
        self.vSplitter = QSplitter(Qt.Vertical)
        self.vSplitter.addWidget(self.topwdidget)
        self.vSplitter.addWidget(self.hSplitter)

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
        self.setCentralWidget(self.vSplitter)
        #### SECONDARY WINDOW
        self.extraWindow = GECSecwindow(self,self.movesList,self.checkedMoves, self.routes,self.curr_route, self.checked_elements_per_route,self.trainerinRoute)
        self.extraWindow.updateroute(self.curr_route)
        self.extraWindow.select_routes.setCurrentText(self.curr_route)
    
    
    
    
    def closeEvent(self, a0: QCloseEvent) -> None:
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
        self.extraWindow.close()
        return super().closeEvent(a0)

    def quit(self):
        self.extraWindow.close()
        self.close()
            
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

    def updateTrainer(self,state,code):
        if state:
            self.trainer_counter += 1
            self.trainerinRoute[self.curr_route].append(code)
            self.counter_row[2].setText(str(self.trainer_counter)+"/"+str(self.totalTrainers))
        else :
            self.trainer_counter -= 1
            self.trainerinRoute[self.curr_route].remove(code)
            self.counter_row[2].setText(str(self.trainer_counter)+"/"+str(self.totalTrainers))


    def updateMons(self,id,color):
        id = id.replace("DEX","")
        
        self.checkedMons[id]=color
        if color == 1:
            self.dex_counter+=1
        elif color == 2: self.dex_counter-=1

        self.counter_row[0].setText(str(self.dex_counter)+"/"+str(self.totalMons))

    def updateItem(self,id,idNumb,state,route):
        if id.startswith("COINS"):
            id = "COINS"
        id = id.replace(" ","").upper()
        print(id)
        ## CASE 1: OLD ITEM/EVENT 
        print(id)
        if state:  ## NEW CHECK: UPDATE COUNTERS, eventually show label
            self.items_counter+=1
            self.checked_elements_per_route[route].append(idNumb)
            ## Update label
            if self.total_checked_elements[id] == 0: # SHOW PIC
                opacity_effect = QGraphicsOpacityEffect() 
                # setting opacity level 
                opacity_effect.setOpacity(1) 
                # adding opacity effect to the label 
                self.itemsPic[id].setGraphicsEffect(opacity_effect) 
            else :#
                if self.itemsPic[id].findChild(QLabel):
                    label = self.itemsPic[id].findChild(QLabel)
                    label.setText(str(self.total_checked_elements[id]+1))
                    label.adjustSize() 
                    label.show()
                else :
                    label = QLabel(str(self.total_checked_elements[id]+1),parent=self.itemsPic[id])
                    label.show()
                
            self.total_checked_elements[id]+=1

        else: ## CHECK REMOVED: REDUCE COUTNER, EVENTUALLY REMOVE LABEL
            self.items_counter-=1
            self.total_checked_elements[id]-=1
            
            self.checked_elements_per_route[route].remove(idNumb)
            if self.total_checked_elements[id]==0 :#FADE LABEL, remove counter
                opacity_effect = QGraphicsOpacityEffect() 
                # setting opacity level 
                opacity_effect.setOpacity(0.5) 
                # adding opacity effect to the label 
                self.itemsPic[id].setGraphicsEffect(opacity_effect)                
            label = self.itemsPic[id].findChild(QLabel)
            if label :
                if self.total_checked_elements[id]<=1:
                    label.hide()
                else:
                    label = self.itemsPic[id].findChild(QLabel)
                    label.setText(str(self.total_checked_elements[id]))
            
        self.counter_row[1].setText(str(self.items_counter)+"/"+str(self.totalMoves))

    
    def updateEvents(self,id,idNumb,state,route):
        ## CASE 1: OLD ITEM/EVENT 
        id = id.replace(" ","").upper()
        if state:  ## NEW CHECK: UPDATE COUNTERS, eventually show label
            self.event_counter+=1   
            self.checked_elements_per_route[route].append(idNumb) 
            ## Update label
            if self.total_checked_elements[id] == 0: # SHOW PIC
                opacity_effect = QGraphicsOpacityEffect() 
                # setting opacity level 
                opacity_effect.setOpacity(1) 
                # adding opacity effect to the label 
                self.itemsPic[id].setGraphicsEffect(opacity_effect) 
                
            else :#ADD COUNTER
                if self.itemsPic[id].findChild(QLabel):
                    label = self.itemsPic[id].findChild(QLabel)
                    label.setText(str(self.total_checked_elements[id]+1))
                    label.adjustSize() 
                    label.show()
                else :
                    label = QLabel(str(self.total_checked_elements[id]+1),parent=self.itemsPic[id])
                    label.show()
            self.total_checked_elements[id]+=1
        else: ## CHECK REMOVED: REDUCE COUTNER, EVENTUALLY REMOVE LABEL
            self.event_counter-=1
            ## Update label
            self.total_checked_elements[id]-=1
            self.checked_elements_per_route[route].remove(idNumb)

            if self.total_checked_elements[id] == 0 :#FADE LABEL, remove counter
                opacity_effect = QGraphicsOpacityEffect() 
                # setting opacity level 
                opacity_effect.setOpacity(0.5) 
                # adding opacity effect to the label 
                self.itemsPic[id].setGraphicsEffect(opacity_effect)
            
            label = self.itemsPic[id].findChild(QLabel)
            if label :
                if self.total_checked_elements[id]<=1:
                    label.hide()
                else:
                    label = self.itemsPic[id].findChild(QLabel)
                    label.setText(str(self.total_checked_elements[id]))
        self.counter_row[4].setText(str(self.event_counter)+"/"+str(self.totalEvents))

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
window.show()
window.extraWindow.show()
app.exec()
