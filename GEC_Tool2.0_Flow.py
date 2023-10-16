from PyQt5.QtWidgets import QSplitter,QWidget,QVBoxLayout,QPushButton, QApplication, QMainWindow, QScrollArea, QSizePolicy, QCheckBox, QHBoxLayout, QGridLayout, QLabel
from PyQt5.QtGui import QPalette, QColor, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QSize
from QTExtra import FlowLayout, ClickableLabel_NotSize
from GECSecWind import GECSecwindow
import os.path as op

import json


class GECWin(QMainWindow):
    def __init__(self):
        super(GECWin, self).__init__()
        self.setWindowTitle("GEC Tool 2.0")
                
        self.monNO=0
        self.dex = []
        self.itemsNO = 0
        self.items=()
        self.movesNO = 0
        self.moves = []
        self.miscNO = 0
        self.vs_NO=0
        self.routes=[]

        with open("routes/Summary.json") as db:
            data = json.load(db)
            self.monNO = data["MonsNO"]
            self.dex = data["Monset"]
            self.itemsNO = data["ItemsNO"]
            self.items = set(data["ItemList"])
            self.miscNO = data["Miscs"]
            self.movesNO=data["MovesNO"]
            self.moves = sorted(data["Moves"])
            self.vs_NO = data["VSNO"]
            self.routes=sorted(data["Routes"])
        self.onTop = True
        self.itemset=[]
        self.moveset=[]
        self.dexset={i:"white" for i in self.dex}
        self.eventset = []
        self.curr_route="pallettown"
        self.itemsinRoute={}
        self.itemsinRoute[self.curr_route]=[]
        self.trainerinRoute={}
        self.trainerinRoute[self.curr_route]=[]
        self.items_counter=0
        self.misc_counter=0
        self.trainer_counter=0
        self.dex_counter=0
        self.current_moves_NO=0
       # self.setWindowFlags(Qt.WindowTransparentForInput)
       # self.setAttribute(Qt.WA_AlwaysStackOnTop, True)
      #  self.extraWindow = GECSecwindow(self.moves)
  #      self.icons=[]
  #      self.moves = []
        self.gridlayout=FlowLayout()
        count=0
        self.movescout=0
        mainlayout = QHBoxLayout()
        ###############################################
        ## self.dex
        ###############################################

        for img in self.dex:
            pic=ClickableLabel_NotSize(img)           
            image=QPixmap("Sprites/mons/"+img.upper()+".png",).scaled(64,64,Qt.KeepAspectRatio)
            pic.setPixmap(image)
            pic.setStyleSheet("background-color: white") 
           # self.icons.append(pic)
            self.gridlayout.addWidget(pic)
            count=count+1
        #self.hSplitter = QGraphicsView(self.scene)
        
        tempW = QWidget()
        tempW.setLayout(self.gridlayout)
        self.dexWidget=QScrollArea()
        self.dexWidget.setWidget(tempW)
        self.dexWidget.setStyleSheet('QWidget{background-color: white}')
        self.dexWidget.setWidgetResizable(True)
        self.dexWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
       
        
        ###############################################
        ## TRANSPARENT WINDOW
        ###############################################
        self.windowWidget = QLabel()

        self.windowWidget.setFocusPolicy(Qt.NoFocus)
        self.windowWidget.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.windowWidget.setAttribute(Qt.WA_TranslucentBackground, True)

        ###############################################
        ## ITEM LIST
        ############################################### 
        self.secWidget = QLabel("TEST")
        self.secWidget.setStyleSheet("background-color: white") 
        

        ################################################
        ## HORIZONTAL SPLITTER
        ##############################################
        self.hSplitter = QSplitter()
        #self.hSplitter.setLayout(self.mainLayout)
        self.hSplitter.addWidget(self.secWidget)
        self.hSplitter.addWidget(self.windowWidget)
        self.hSplitter.addWidget(self.dexWidget)
        self.hSplitter.setStretchFactor(0,1)
        self.hSplitter.setStretchFactor(1,25)
        self.hSplitter.setStretchFactor(2,1)
       

       ################################################
        ## SUMMARY WINDOW (TOP)
        ############################################## 
        self.deximage = ClickableLabel_NotSize('dexCount')
        self.deximage.setPixmap(QPixmap("Sprites/ball.png"))
        self.deximage.setScaledContents(False)
        self.itemImage=ClickableLabel_NotSize('itemsCount')
        self.itemImage.setPixmap(QPixmap("Sprites/potion.png"))
        self.itemImage.setScaledContents(False)
        self.trainerImage=ClickableLabel_NotSize('TrainersCount')
        self.trainerImage.setPixmap(QPixmap("Sprites/VS_Seeker.png"))
        self.trainerImage.setScaledContents(False)
        self.moveImage=ClickableLabel_NotSize('movesCount')
        self.moveImage.setPixmap(QPixmap("Sprites/moves.png"))
        self.moveImage.setScaledContents(False)
        self.miscImage=ClickableLabel_NotSize('MiscCount')
        self.miscImage.setPixmap(QPixmap("Sprites/leftovers.png"))
        self.miscImage.setScaledContents(False)
        self.img_row = [self.deximage,self.itemImage,self.trainerImage,self.moveImage,self.miscImage]
        self.counter_row = [
            QLabel(str(self.dex_counter)+"/"+str(self.monNO)),
            QLabel(str(self.items_counter)+"/"+str(self.itemsNO)),
            QLabel(str(self.trainer_counter)+"/"+str(self.vs_NO)),
            QLabel(str(self.current_moves_NO)+"/"+str(self.movesNO)),
            QLabel(str(self.misc_counter)+"/"+str(self.miscNO))
        ]
        topgrid = QGridLayout()
        for i in range(0,5):

            box=QHBoxLayout()
            tempwidget=QWidget()
            box.addWidget(self.img_row[i],alignment=Qt.AlignCenter)
            box.addWidget(self.counter_row[i],alignment=Qt.AlignCenter)
            tempwidget.setLayout(box)
            topgrid.addWidget(tempwidget,0,i)
#            topgrid.addWidget(img_row[i],0,i*2,alignment=Qt.AlignCenter)
            #self.img_row[i].setStyleSheet("background-color: red")
            #self.counter_row[i].setStyleSheet("background-color: red")
            #tempwidget.setStyleSheet("background-color: blue")
            tempwidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            topgrid.setColumnStretch(i,0)
        topgrid.setRowStretch(0,0)
        
#            self.counter_row[i].setScaledContents(False)
#            topgrid.addWidget(self.counter_row[i],0,i*2+1)
        self.topwdidget = QWidget()
        self.topwdidget.setLayout(topgrid)
        self.topwdidget.setFixedHeight(self.topwdidget.sizeHint().height())
    
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
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        tmp = QWidget()
        self.magicbutton= QPushButton(tmp)
        self.magicbutton.setText("Test")
        self.magicbutton.clicked.connect(self.changeflags)

        tmp2 = QWidget()
        self.closeButton = QPushButton(tmp2)
        self.closeButton.setText("Chiudi")
        self.closeButton.clicked.connect(self.quit)

        self.statusBar().setStyleSheet("background-color: white")
        self.statusBar().addWidget(self.closeButton)
        self.statusBar().addWidget(self.magicbutton)

        self.setCentralWidget(self.vSplitter)
    
    def updatemoves(self,b):
        print(b)


    def quit(self):
        self.close()

    def changeflags(self):
        if self.onTop:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.onTop = False
        else:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            self.onTop = True
        self.show()

   
app = QApplication([])

window = GECWin()
window.showMaximized()
app.exec()
