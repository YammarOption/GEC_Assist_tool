from PyQt5 import QtGui
from PyQt5.QtWidgets import ( QSplitter,QWidget, QApplication, QMenuBar, 
                            QScrollArea, QProgressDialog, QHBoxLayout, QGridLayout, QLabel,
                            QDesktopWidget,QGraphicsColorizeEffect)
from PyQt5.QtGui import QPixmap, QCloseEvent, QFont, QColor
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from QTExtra import FlowLayout, ClickableLabel_NotSize,ClickableLabel, next_color
from GECSecWind import GECSecwindow
from qframelesswindow import FramelessMainWindow
import os.path as op

import json


# TODO: - TEST PER VEDERE TRADUZIONE
# SELECT GAME SCREEN
#       - CHECK TOTAL NUMBER + GLITCH?
#       - BETTER STYLE

#       - CHANGE FLOW WITH EXPANDING

class GECWin(FramelessMainWindow):
    updateSignal = pyqtSignal(int)

    def __init__(self):
        super(GECWin, self).__init__()
    
    def setup(self):
        self.setWindowTitle("GEC Tool 2.0")
       
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
        self.updateSignal.emit(10)

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
        # self.progress.setValue(20)

        self.dexlayout=QGridLayout()
        self.itemlayout =QGridLayout()
        self.movescout=0
        ###############################################
        ## DEX
        ###############################################

        # for img in dexList:
        #     pic=ClickableLabel_NotSize("DEX"+img,self,self.checkedMons[img])           
        #     image=QPixmap("Sprites/mons/"+img.upper()+".png",).scaled(64,64,Qt.KeepAspectRatio)
        #     pic.setPixmap(image)
        #     pic.setStyleSheet("background-color: "+ next_color[self.checkedMons[img]]) 
        #    # self.icons.append(pic)
        #     self.dexlayout.addWidget(pic)
        
        count=0
        for img in dexList:
            pic=ClickableLabel("DEX"+img,self,self.checkedMons[img])
            image=QPixmap("Sprites/mons/"+img.upper()+".png",)#.scaled(64,64,Qt.KeepAspectRatio)
            pic.setPixmap(image)
           # pic.setStyleSheet("border: 3px solid "+ next_color[self.checkedMons[img]]) 
           # self.icons.append(pic)
            pic.setGraphicsEffect(next_color(self.checkedMons[img]))
            self.dexlayout.addWidget(pic,int(count/8), count%8)
            count=count+1
        self.dexWidget=QWidget()
        self.dexWidget.setLayout(self.dexlayout)
        self.dexWidget.setStyleSheet('QWidget{background-color: white}')
        
        # self.progress.setValue(30)

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
                self.itemlayout.addWidget(QLabel(""),int(count/10), count%10)            
                count=count+1
            else:

                pic=ClickableLabel("ITEM"+item)
                image=QPixmap("Sprites/items/"+itemList[count][item][0]).scaled(100,100,Qt.KeepAspectRatio)
                self.itemsPic[item.replace(" ","").upper()] = pic
                pic.setPixmap(image)
                if self.total_checked_elements[item.replace(" ","").upper()] <1:
                    color_effect = QGraphicsColorizeEffect() 
                    # setting opacity level 
                    color_effect.setColor(QColor(128,128,128)) 
                    # adding opacity effect to the label 
                    pic.setGraphicsEffect(color_effect) 
                elif  self.total_checked_elements[item.replace(" ","").upper()] >1:
                    label = QLabel(str(self.total_checked_elements[item.replace(" ","").upper()]),parent=self.itemsPic[item.replace(" ","").upper()])
                    label.show()
                ## Add eventual label
                self.itemlayout.addWidget(pic,int(count/10), count%10)            
                count=count+1
        

        self.itemwidget=QScrollArea()
        self.itemwidget.setLayout(self.itemlayout)
        self.itemwidget.setStyleSheet('QWidget{background-color: white}')
        # self.progress.setValue(40)

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
            QLabel(str(self.dex_counter)+"/"+str(self.totalMons)),
            QLabel(str(self.items_counter)+"/"+str(self.totalMoves)),
            QLabel(str(self.trainer_counter)+"/"+str(self.totalTrainers)),
            QLabel(str(self.moves_counter)+"/"+str(self.TotalMoves)),
            QLabel(str(self.event_counter)+"/"+str(self.totalEvents))
        ]
        # Filling the grid
        topgrid = QHBoxLayout()
        topgrid.addWidget(QLabel(""))
        for i in range(0,5):
            box=QHBoxLayout()
            tempwidget=QWidget()
            box.addWidget(self.img_row[i],alignment=Qt.AlignCenter)
            box.addWidget(self.counter_row[i],alignment=Qt.AlignCenter)
            self.counter_row[i].setFont(QFont("Sanserif", 15))
            tempwidget.setLayout(box)
            topgrid.addWidget(tempwidget)
            #tempwidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            tempwidget.setMaximumSize(tempwidget.sizeHint())
            #topgrid.setColumnStretch(i+1,0)
#        topgrid.setRowStretch(0,0)
        topgrid.addWidget(QLabel(""),)

        self.topwdidget = QWidget()
        self.topwdidget.setLayout(topgrid)    
        self.topwdidget.setStyleSheet("background-color: white")
        ################################################
        ## Vertical splitter
        ##############################################
        self.vSplitter = QSplitter(Qt.Vertical)
        self.vSplitter.addWidget(self.topwdidget)
        self.vSplitter.addWidget(self.hSplitter)
        # self.progress.setValue(50)

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
        if id.startswith("GETTONI"):
            id = "GETTONI"
        id = id.replace(" ","").upper()
        ## CASE 1: OLD ITEM/EVENT 
        try :
            if state:  ## NEW CHECK: UPDATE COUNTERS, eventually show label
                self.items_counter+=1
                self.checked_elements_per_route[route].append(idNumb)
                ## Update label
                if self.total_checked_elements[id] == 0: # SHOW PIC
                    color_effect = QGraphicsColorizeEffect() 
                    # setting opacity level 
                    color_effect.setStrength(0) 
                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect) 
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
                    color_effect = QGraphicsColorizeEffect() 
                    # setting opacity level 
                    color_effect.setColor(QColor(128,128,128)) 
                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect)                
                label = self.itemsPic[id].findChild(QLabel)
                if label :
                    if self.total_checked_elements[id]<=1:
                        label.hide()
                    else:
                        label = self.itemsPic[id].findChild(QLabel)
                        label.setText(str(self.total_checked_elements[id]))
        except Exception as err:
            print("Exc "+str(err))
        self.counter_row[1].setText(str(self.items_counter)+"/"+str(self.totalMoves))

    
    def updateEvents(self,id,idNumb,state,route):
        ## CASE 1: OLD ITEM/EVENT 
        id = id.replace(" ","").upper()
        try:
            if state:  ## NEW CHECK: UPDATE COUNTERS, eventually show label
                self.event_counter+=1   
                self.checked_elements_per_route[route].append(idNumb) 
                ## Update label
                if self.total_checked_elements[id] == 0: # SHOW PIC
                    color_effect = QGraphicsColorizeEffect() 
                    # setting opacity level 
                    color_effect.setStrength(0) 
                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect) 
                    
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
                    color_effect = QGraphicsColorizeEffect() 
                    # setting opacity level 
                    color_effect.setColor(QColor(128,128,128))                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect)
                
                label = self.itemsPic[id].findChild(QLabel)
                if label :
                    if self.total_checked_elements[id]<=1:
                        label.hide()
                    else:
                        label = self.itemsPic[id].findChild(QLabel)
                        label.setText(str(self.total_checked_elements[id]))
        except Exception as err:
            print("Exc: "+str(err))
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
window.setup()
window.show()
window.extraWindow.show()
app.exec()
