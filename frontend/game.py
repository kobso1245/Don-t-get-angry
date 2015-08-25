from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import sys
from time import sleep


class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI(0)

    def __build_square(self, boxes, i, horiz, vert, color):
        boxes.append(QFrame(self))
        boxes[i].setGeometry(horiz,vert,30,30)
        boxes[i].setStyleSheet("QWidget {background-color: %s }" % color.name())


    def initUI(self, p):
        self.boxes = []
        self.presses = 0
        
        
        for i in range(0,7):
            self.__build_square(self.boxes, i, 335, 545-(i%15)*35, QColor(255,0,0)) 
        for i in range(7,13):
            self.__build_square(self.boxes, i, 370 + (i-7)*35,335, QColor(255,0,0)) 
        self.__build_square(self.boxes, 13, 545,300, QColor(0,0,255)) 

        for i in range(14,20):
            self.__build_square(self.boxes, i, 265 + (22 - i)*35,265, QColor(0,0,255)) 
        for i in range(20,27):
            self.__build_square(self.boxes, i, 335, 265 - (i-20)*35, QColor(0,0,255)) 
        self.__build_square(self.boxes, 27, 300, 55, QColor(255,0,255)) 

        for i in range(28,35):
            self.__build_square(self.boxes, i, 265, 55+(i - 28)*35, QColor(255,0,255)) 
        for i in range(35,41):
            self.__build_square(self.boxes, i, 230 - (i - 35)*35,265, QColor(255,0,255)) 
        self.__build_square(self.boxes, 41, 55,300, QColor(0,255,255)) 
       
        for i in range(42, 49):
            self.__build_square(self.boxes, i, 55 + (i - 42)*35 ,335, QColor(0,255,255)) 
        for i in range(49,55):
            self.__build_square(self.boxes, i, 265, 370 + (i - 49)*35, QColor(0,255,255)) 
        self.__build_square(self.boxes, 55,300, 545, QColor(255,0,0)) 
       
        #inner parts
        for i in range(56, 62):
            self.__build_square(self.boxes, i,300, 510 - (i - 56)*35, QColor(200,0,0)) 
        for i in range(62,68):
            self.__build_square(self.boxes, i, 510 - (i - 62)*35, 300, QColor(0,0,200)) 
        for i in range(68,74):
            self.__build_square(self.boxes, i, 300, 90 + (i-68)*35, QColor(200,0,200)) 
        for i in range(74,80):
            self.__build_square(self.boxes, i, 90 + (i-74)*35,300, QColor(p,200,200))

        self.setGeometry(600,900,900,600)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

        if e.key() == Qt.Key_Space:
            self.boxes[self.presses].setStyleSheet("QWidget {background-color: %s }" % QColor(0,0,0).name())
            self.presses += 1


app = QApplication(sys.argv)
widg = Table()
app.exec_()
