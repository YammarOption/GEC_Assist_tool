from PyQt5.QtWidgets import QWidget,QVBoxLayout, QApplication, QMainWindow, QScrollArea, QSizePolicy, QCheckBox, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize
from QTExtra import FlowLayout, ClickableLabel_NotSize
from GECSecWind import GECSecwindow
import os.path as op

import json


class GECWin(QMainWindow):
    def __init__(self,dex,moves):
        super(GECWin, self).__init__()
        self.setWindowTitle("GEC Tool 2.0")
      #  self.extraWindow = GECSecwindow(moves)
  #      self.icons=[]
  #      self.moves = []
        self.gridlayout=FlowLayout()
        count=0
        self.movescout=0
        mainlayout = QHBoxLayout()
     ### POKEDEX #######

        for img in dex:
            pic=ClickableLabel_NotSize(img)
            image=QPixmap("Sprites/mons/"+img.upper()+".png",).scaled(64,64,Qt.KeepAspectRatio)
            pic.setPixmap(image)
            pic.setStyleSheet("background-color: white") 
           # self.icons.append(pic)
            self.gridlayout.addWidget(pic)
            count=count+1
        #self.mainWidget = QGraphicsView(self.scene)
        tempW = QWidget()
        tempW.setLayout(self.gridlayout)
        DexWidget=QScrollArea()
        DexWidget.setWidget(tempW)
        DexWidget.setWidgetResizable(True)
        DexWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        #######
        ###### MOVES LISTBOX
        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(tempW)
        self.mainWidget=QWidget()
        self.mainWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.mainWidget.setLayout(self.gridlayout)
        self.setCentralWidget(self.mainWidget)
    
    def updateMoves(self,b):
        
        print(b)


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

app = QApplication([])

window = GECWin(dex,moves)
window.show()
app.exec()
