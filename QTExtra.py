#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import (QLabel, QLayout, QSizePolicy, QCheckBox, QGraphicsColorizeEffect )
from PyQt5.QtGui import QPainter, QColor, QPaintEvent, QPixmap

colors={2:QColor(0,0,192),0:QColor(0,0,0)}

def next_color(i:int):
    effect = QGraphicsColorizeEffect()
    if i == 1:
        effect.setStrength(0)
    else:
        effect.setColor(colors[i])
    return effect

class MyCheckbox(QCheckBox):
    def __init__(self, name,id , parent,code=0):
        QCheckBox.__init__(self, parent)
        self.id = id
        self.name = name
        self.parent=parent
        self.code = id.upper().replace(" ","") + str(code).upper()
        self.setText(name)


class ClickableLabel(QLabel):
    def __init__(self, id, parent=None,code = 0):
        QLabel.__init__(self, parent)
        self.parent = parent
        self.id = id
        self.code=code
        self.image=None
        self.setScaledContents(True)
    
    def mouseReleaseEvent(self, event):
        if not self.id.startswith("DEX"):
            return
        self.code=(self.code+1)%3

        #self.setStyleSheet("border: 3px solid " + next_color[self.code])
        self.setGraphicsEffect(next_color(self.code))
        self.parent.updateMons(self.id,self.code)

    def setPixmap(self, pixmap: QPixmap) -> None:
        self._pixmap = pixmap
        self.repaint()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        if self._pixmap is not None:
            imageWidth, imageHeight = self._pixmap.width(), self._pixmap.height()
            labelWidth, labelHeight = self.width(), self.height()
            ratio = min(labelWidth / imageWidth, labelHeight / imageHeight)
            newWidth, newHeight = int(imageWidth * ratio), int(imageHeight * ratio)
            newPixmap = self._pixmap.scaledToWidth(newWidth, Qt.TransformationMode.FastTransformation)
            x, y = abs(newWidth - labelWidth) // 2, abs(newHeight - labelHeight) // 2
            QPainter(self).drawPixmap(x, y, newPixmap)



class ClickableLabel_NotSize(QLabel):
    def __init__(self, id, parent=None,code=0):
        QLabel.__init__(self, parent)
        self.parent = parent
        self.id = id
        self.code=code
        self.image=None
        self.setScaledContents(True)

    def mouseReleaseEvent(self, event):
        if not self.id.startswith("DEX"):
            return
        self.code=(self.code+1)%3
        self.setStyleSheet("background-color:" + next_color[self.code])
        self.parent.updateMons(self.id,self.code)



class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()
