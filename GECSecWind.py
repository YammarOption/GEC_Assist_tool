from PyQt5.QtWidgets import QWidget,QVBoxLayout, QApplication, QMainWindow, QScrollArea, QLabel, QCheckBox, QHBoxLayout, QGraphicsScene
from PyQt5.QtGui import QPalette, QColor, QPixmap, QCloseEvent
from PyQt5.QtCore import Qt, QSize
from QTExtra import FlowLayout,ClickableLabel
import os.path as op

import json


class GECSecwindow(QMainWindow):
    def __init__(self,parent,moves):
        super(GECSecwindow, self).__init__()
        self.setWindowTitle("GEC Tool 2.0 AA")
        self.parent = parent
        self.moves = moves

        #######
        ###### MOVES LISTBOX
        moveWidget = QWidget()
        moveWidgetLayout = QVBoxLayout()
        moveheader = QLabel("Move List")
        moveWidgetLayout.addWidget(moveheader)
        movelist=QWidget()
        movelistLayout=QVBoxLayout()
        for move in moves:  
            Chbox = QCheckBox(move)
            Chbox.stateChanged.connect(self.parent.updateMoves)
            movelistLayout.addWidget(Chbox)
        movelist.setLayout(movelistLayout)
        moveWidgetLayout.addWidget(movelist)
        moveWidget.setLayout(moveWidgetLayout)
        moveArea =QScrollArea()
        moveArea.setWidget(moveWidget)
        moveArea.setWidgetResizable(True)
        moveArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mainlayout = QHBoxLayout()
        self.mainlayout.addWidget(moveArea)
        self.mainWidget=QWidget()
        self.mainWidget.setLayout(self.mainlayout)
        self.setCentralWidget(self.mainWidget)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.parent.close()
        return super().closeEvent(a0)