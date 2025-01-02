from PyQt5 import QtGui
from PyQt5.QtWidgets import ( QSplitter,QWidget, QMenuBar, QHBoxLayout,QVBoxLayout, QScrollArea, QLabel,
                            QDesktopWidget,QGraphicsColorizeEffect, QGraphicsOpacityEffect,QSizePolicy)
from PyQt5.QtGui import QPixmap, QCloseEvent, QFont, QColor
from PyQt5.QtCore import Qt, QPoint,pyqtSignal,pyqtSlot
from .QTExtra import ClickableLabel_NotSize, next_color,FlowLayout
from .GECSecWind import GECSecwindow
from qframelesswindow import FramelessMainWindow
from ..Twitch_plays.TwitchGECController import  TwitchGECController
from ..mgba.GameMonitorServer import GameMonitorServer
from ..Game import Game
import os.path as op
import configparser
import json

class GECRegularWindow(FramelessMainWindow):
    twitchSignal = pyqtSignal(str,str) 
    gameSignal = pyqtSignal(str,str) 

    def __init__(self,game:Game):
        super(GECRegularWindow, self).__init__()
        self.game = game

    def setup(self,config:configparser.ConfigParser):
        self.setWindowTitle("GET 2.7")
        self.setWindowIcon(QtGui.QIcon('Datapack/Sprites/icon.png'))
        self.config = config
        self.monitor = self.config.getboolean("GAME MONITOR","USE_MONITOR")
        self.twitch = self.config.getboolean("TWITCH INTEGRATION","USE_TWITCH")
        self.onTop = False
        self.icons=[]
        self.itemsPic={}
        self.dexlayout=FlowLayout()
        self.itemlayout = FlowLayout()
        self.movescout=0
        ###############################################
        ## DEX
        ###############################################

        self.dexPics={}
        for img in self.game.dexList:
            img=img.upper()
            if img == "VOID":
                pic=QLabel()
                image=QPixmap("Datapack/Sprites/items/blank.png")
                pic.setPixmap(image)     
                self.dexlayout.addWidget(pic)

                continue
            pic=ClickableLabel_NotSize("DEX"+img,self,self.game.checkedMons[img])
            pic.setToolTip(img)
            self.dexPics[img.upper()]=pic
            image=QPixmap("Datapack/Sprites/mons/"+img+".png")
            pic.setPixmap(image)
            self.icons.append(pic)
            pic.setGraphicsEffect(next_color(self.game.checkedMons[img]))
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

        ################################################
        ## SUMMARY WINDOW (TOP)
        ############################################## 
        # Reading the data
        self.deximage = ClickableLabel_NotSize('dexCount')
        self.deximage.setPixmap(QPixmap("Datapack/Sprites/ball.png"))
        self.deximage.setScaledContents(False)
        self.itemImage=ClickableLabel_NotSize('itemsCount')
        self.itemImage.setPixmap(QPixmap("Datapack/Sprites/strum.png"))
        self.itemImage.setScaledContents(False)
        self.trainerImage=ClickableLabel_NotSize('TrainersCount')
        self.trainerImage.setPixmap(QPixmap("Datapack/Sprites/VS_Seeker.png"))
        self.trainerImage.setScaledContents(False)
        self.moveImage=ClickableLabel_NotSize('movesCount')
        self.moveImage.setPixmap(QPixmap("Datapack/Sprites/moves.png"))
        self.moveImage.setScaledContents(False)
        self.miscImage=ClickableLabel_NotSize('MiscCount')
        self.miscImage.setPixmap(QPixmap("Datapack/Sprites/Ribbon.png"))
        self.miscImage.setScaledContents(False)
        self.img_row = [self.deximage,self.itemImage,self.trainerImage,self.moveImage,self.miscImage]
        self.counter_row = [
            QLabel("{:03d}".format(self.game.dex_counter)+"/"+"{:03d}".format(self.game.totalMons)),
            QLabel("{:03d}".format(self.game.items_counter)+"/"+"{:03d}".format(self.game.totalItems)),
            QLabel("{:03d}".format(self.game.trainer_counter)+"/"+"{:03d}".format(self.game.totalTrainers)),
            QLabel("{:03d}".format(self.game.moves_counter)+"/"+"{:03d}".format(self.game.totalMoves)),
            QLabel("{:03d}".format(self.game.event_counter)+"/"+"{:03d}".format(self.game.totalEvents))]
        # Filling the grid
        topgrid = QHBoxLayout()
        for i in range(0,5):
            box=QHBoxLayout()
            tempwidget=QWidget()
            box.addWidget(self.img_row[i],alignment=Qt.AlignRight)
            box.addWidget(self.counter_row[i],alignment=Qt.AlignLeft)
            self.counter_row[i].setFont(QFont("Sanserif", 12))
            self.counter_row[i].setMaximumSize(self.counter_row[i].maximumSize())
            self.counter_row[i].setFixedSize(self.counter_row[i].maximumSize())
            tempwidget.setLayout(box)
            topgrid.addWidget(tempwidget)
        self.topwdidget = QWidget()
        if self.monitor:
            self.monitorLabels=[]
            monitorlayout= QHBoxLayout()
            layout:list = self.game.getGameMonitorlayout()
            i=0
            while i<len(layout):
                picLabel=QLabel()
                picLabel.setPixmap(QPixmap(layout[i]))         
                dataLabel = QLabel(layout[i+1])
                dataLabel.setFont(QFont("Sanserif", 12,QFont.Bold))  
                dataLabel.setMaximumSize(dataLabel.maximumSize())
                dataLabel.setFixedSize(dataLabel.maximumSize())
                self.monitorLabels.append(dataLabel)
                monitorlayout.addWidget(picLabel,alignment=Qt.AlignRight,stretch=1)
                monitorlayout.addWidget(dataLabel,alignment=Qt.AlignLeft,stretch=1)
                i+=2
            if len(layout)<10:
                monitorlayout.addWidget(QLabel(),stretch=10-len(layout))
            upwidget = QWidget()
            upwidget.setLayout(topgrid)
            upwidget.setMaximumHeight(topgrid.totalMinimumSize().height()) 
            downwidget = QWidget()
            downwidget.setLayout(monitorlayout)
            downwidget.setMaximumHeight(monitorlayout.totalMinimumSize().height()) 
            line = QWidget()
            line.setFixedHeight(4)
            line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            line.setStyleSheet("background-color: rgb(240,240,240);")
            fullgrid = QVBoxLayout()
            fullgrid.addWidget(upwidget)
            fullgrid.addWidget(line)
            fullgrid.addWidget(downwidget)
            fullgrid.setContentsMargins(0,0,0,0)
            fullgrid.setSpacing(0)
            self.topwdidget.setLayout(fullgrid)
            self.topwdidget.setMaximumHeight(fullgrid.totalMinimumSize().height()) 
        else : 
            self.topwdidget.setLayout(topgrid)
            self.topwdidget.setMaximumHeight(topgrid.totalMinimumSize().height()) 

        #self.topwdidget.setMinimumWidth(topgrid.totalMinimumSize().width()) 
        self.topwdidget.setStyleSheet("background-color: white")
        ################################################
        ## Vertical splitter
        ##############################################
        self.vSplitter = QSplitter(Qt.Vertical)
        self.vSplitter.addWidget(self.topwdidget)
        self.vSplitter.addWidget(self.windowWidget)
        self.vSplitter.setStretchFactor(0,1)
        self.vSplitter.setStretchFactor(1,1)

        ###############################################
        ## ITEM LIST
        ############################################### 
        count=0
        for couple in self.game.itemList:
            item =list(couple.keys())[0]
            if item == "blank" or item == "VOID":
                pic=QLabel()
                image=QPixmap("Datapack/Sprites/items/blank.png")
                pic.setPixmap(image)     
                self.itemlayout.addWidget(pic)
                count=count+1
                continue
            pic=ClickableLabel_NotSize("ITEM"+item)
            pic.setToolTip(item)
            image=QPixmap("Datapack/Sprites/items/"+self.game.itemList[count][item][0])
            self.itemsPic[item.replace(" ","").upper()] = pic
            pic.setPixmap(image)
            if item.startswith("PKRS_") and \
                self.game.total_checked_elements[item.replace(" ","").upper()][0] < self.game.total_checked_elements[item.replace(" ","").upper()][1]:
                color_effect = QGraphicsOpacityEffect() 
                # setting opacity level 
                color_effect.setOpacity(0) 
                # adding opacity effect to the label 
                pic.setGraphicsEffect(color_effect) 
            else:
                label = QLabel(str(self.game.total_checked_elements[item.replace(" ","").upper()][0]),parent=self.itemsPic[item.replace(" ","").upper()])
                label.setStyleSheet("background-color: rgba(0,0,0,0%)")
                label.setFont(QFont("Sanserif", 7,QFont.Bold))
                #REMOVE COLOR IF NOT GET YET
                if self.game.total_checked_elements[item.replace(" ","").upper()][0] < self.game.total_checked_elements[item.replace(" ","").upper()][1]:
                    color_effect = QGraphicsColorizeEffect() 
                    # setting opacity level 
                    color_effect.setColor(QColor(0,0,0)) 
                    pic.setGraphicsEffect(color_effect)
                    pic.setStyleSheet("QToolTip { color: red }")

                # MORE THAN ONE  OBTAINED: SHOW LABLE
                if self.game.total_checked_elements[item.replace(" ","").upper()][0] >self.game.total_checked_elements[item.replace(" ","").upper()][1]: 
                    label.show()
                else: label.hide() #EXACTLY ONE OBTAINED: ONLY COLOR, NO LABEL

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
        menuBar.addAction('Close',self.quit)
        menuBar.addAction('Lock/Unlock',self.changeflags)
        self.titleBar.layout().insertStretch(1, 1)
        self.titleBar.layout().insertWidget(1, menuBar, 10, Qt.AlignRight)
        self.setMenuWidget(menuBar)
        self.statusBar().setStyleSheet("background-color: white")
        self.setCentralWidget(self.hSplitter)

        #### SECONDARY WINDOW
        self.extraWindow = GECSecwindow(self,self.game.movesList,self.game.checkedMoves, self.game.routes,self.game.curr_route, self.game.checked_elements_per_route,self.game.trainerinRoute)
        self.extraWindow.updateroute(self.game.curr_route)
        self.extraWindow.colorAllCombobox()

        ##########################
        ##  TWITCH CONTROLLER
        #########################
        if self.twitch:
            self.twitchSignal.connect(self.twitchUpdate)
            self.TwitchController=TwitchGECController(self.twitchSignal,self.config)
            self.TwitchController.start()

        ##########################
        ##  GAME MONITOR
        #########################
        
        if self.monitor: 
            self.gameSignal.connect(self.gameUpdate)
            self.gameMonitor=GameMonitorServer(self.gameSignal,self.config)
            self.gameMonitor.start()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.game.save()
        self.extraWindow.close()
        if self.twitch:
            self.TwitchController.quit()
        if self.monitor:
            self.gameMonitor.close()
        return super().closeEvent(a0)

    def quit(self):
        self.game.save()
        self.extraWindow.close()
        if self.twitch:
            self.TwitchController.quit()
        if self.monitor:
            self.gameMonitor.close()
        self.close()
            
    def changeflags(self):
        if self.onTop:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.onTop = False
        else:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            self.onTop = True
        self.show()

    def updateMons(self,id,color):
        id = id.replace("DEX","")
        self.game.updateMons(id,color==1)
        #check if pokemon is connected to an event
        # The xor allows the if to be entered only in two case: if we are coloring the icon AND we haven't marked the pokemon yet
        # OR if we have removing the colored and the mon is already colored
        if ((color == 1) ^ (self.game.checkedMons[id]==1)) and self.game.checkEventForMon(id):
            self.updateElements(self.game.getEventForMon(id),"",color==1,self.game.curr_route,False)
        self.counter_row[0].setText("{:03d}".format(self.game.dex_counter)+"/"+"{:03d}".format(self.game.totalMons))
        self.game.checkedMons[id]=color

    def twitchUpdateMons(self,id,update):
        ids = id.split(",")
        for i in ids:     
            if i in self.dexPics:
                self.dexPics[i].twitchUpdate(update)
                self.updateMons(i,update)

    def updateMoves(self,move,state):
        self.game.updateMoves(move,state)
        self.counter_row[3].setText("{:03d}".format(self.game.moves_counter)+"/"+"{:03d}".format(self.game.totalMoves))

    def twitchUpdateMove(self,move,state):
        moves = move.split(",")
        for m in moves:
            if m.upper() not in (name.upper().replace(" ","") for name in self.game.movesList): continue
            self.updateMoves(m,state)
            self.extraWindow.twitchUpdateMoves(m,state)

    def twitchUpdateTrainer(self,state,code):
        code=self.extraWindow.twitchUpdateTrainers(code,state)
        if code == "": return
        self.updateTrainer(state,code)

    def updateTrainer(self,state,code):
        self.game.updateTrainer(state,code)
        self.counter_row[2].setText("{:03d}".format(self.game.trainer_counter)+"/"+"{:03d}".format(self.game.totalTrainers))

    def updateElements(self,id,idNumb,state,route,item=True):
        ## CASE 1: OLD ITEM/EVENT 
        id = id.replace(" ","").upper().replace("(H)","").replace("($)","")
        if self.game.checkEventForItem(id):
            self.updateElements(self.game.getEventForItem(id),"",state,route,False)
            #rename to remove the prefix that activated the check for events
            id = self.game.renameElement(id)
        id = self.game.renameElement(id)
        if item:
            self.game.updateItems(id,idNumb,route,state)
        else: self.game.updateEvents(id,idNumb,route,state)
        try :
            if state:  ## NEW CHECK: UPDATE COUNTERS, eventually show label
                if id.startswith("PKRS_") and self.game.total_checked_elements[id][0] == self.game.total_checked_elements[id][1]:
                    color_effect = QGraphicsOpacityEffect() 
                    # setting opacity level 
                    color_effect.setOpacity(100) 
                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect)
                elif self.game.total_checked_elements[id][0] == self.game.total_checked_elements[id][1]:
                    color_effect = QGraphicsColorizeEffect() 
                    color_effect.setStrength(0)
                    self.itemsPic[id].setStyleSheet("QToolTip { color: black}")
                    self.itemsPic[id].setGraphicsEffect(color_effect) 
                elif  self.game.total_checked_elements[id][0] > self.game.total_checked_elements[id][1]:
                    label = self.itemsPic[id].findChild(QLabel)
                    label.setText(str(self.game.total_checked_elements[id][0]))
                    label.adjustSize() 
                    label.show()
            else: ## CHECK REMOVED: REDUCE COUNTER, EVENTUALLY REMOVE LABEL
                label = self.itemsPic[id].findChild(QLabel)
                if id.startswith("PKRS_") and self.game.total_checked_elements[id][0] < self.game.total_checked_elements[id][1]:
                    color_effect = QGraphicsOpacityEffect() 
                    # setting opacity level 
                    color_effect.setOpacity(0) 
                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect)
                elif self.game.total_checked_elements[id][0] > self.game.total_checked_elements[id][1]:#Reduce LABEL, remove counterù
                    label.setText(str(self.game.total_checked_elements[id][0]))
                elif self.game.total_checked_elements[id][0] == self.game.total_checked_elements[id][1]:
                    label.hide()
                elif self.game.total_checked_elements[id][0] < self.game.total_checked_elements[id][1]:
                    color_effect = QGraphicsColorizeEffect() 
                    # setting opacity level 
                    color_effect.setColor(QColor(0,0,0))
                    self.itemsPic[id].setStyleSheet("QToolTip { color: red}")
                    # adding opacity effect to the label 
                    self.itemsPic[id].setGraphicsEffect(color_effect) 
        except Exception as err:
           print("Exc: "+str(err))
        if item: 
            self.counter_row[1].setText("{:03d}".format(self.game.items_counter)+"/"+"{:03d}".format(self.game.totalItems))
        else :
            self.counter_row[4].setText("{:03d}".format(self.game.event_counter)+"/"+"{:03d}".format(self.game.totalEvents))

    def twitchUpdateCollectibles(self,name,state,prefix):
            id,idNumb,route=self.extraWindow.twitchUpdateCollectibles(name,state,prefix)
            if not id: return
            self.updateElements(id,idNumb,state,route,prefix=="ITEM-")

    def updateRoute(self,route):
        self.game.curr_route=route

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
            self.game.save() 

    @pyqtSlot(str,str)
    def gameUpdate( self, datatype, data ):
        if not datatype == "GAMELOG" : return
        updates = self.game.updateGameMonitorlayout(data)
        print(len(self.monitorLabels))
        for i in range(len(self.monitorLabels)):
            if  isinstance( self.monitorLabels[i], QLabel):
                self.monitorLabels[i].setText(updates[i])

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
   
