from PyQt5.QtWidgets import QLabel, QComboBox, QMainWindow,QApplication, QWidget, QFrame, QProgressBar, QPushButton, QLCDNumber, QVBoxLayout, QCheckBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QBasicTimer,  QRect,pyqtSignal, QObject
import sys
from random import randrange
from time import sleep

class Communicate(QObject):
    show_button = pyqtSignal()

class Popup(QWidget):
    def __init__(self, main_win):
        super().__init__()
        self.initUI(main_win)

    def initUI(self, main_win):
        self.main_win = main_win
        self.button_yes = QPushButton('Yes', self)
        self.button_no = QPushButton('No', self)
        self.button_yes.move(20,10)
        self.button_no.move(150,10)
        self.button_yes.clicked.connect(self._say_yes)
        self.button_no.clicked.connect(self._say_no)
        self.setGeometry(300,300,300,50)
        self.setWindowTitle('Would you like a new figure?')
        self.show()

    def _say_yes(self):
        self.main_win.roll_dice_button.setEnabled(False)
        self.main_win.draw_figure(self.main_win.player_starting_pos, (255,0,0), 1)
        self.main_win.answer = True
        if self.main_win.last_throws[0] == 6:
            self.main_win.last_throws = (0,
                                         self.main_win.last_throws[1])
            self.close()
            return
        self.main_win.last_throws = (self.main_win.last_throws[0],
                                     0)
        self.main_win._Table__add_checkbox(0)
        self.main_win.figures.append(0)
        self.close()
        [checkbox.setCheckable(True) for checkbox in self.main_win.checkboxes]

    def _say_no(self):
        self.main_win.roll_dice_button.setEnabled(False)
        self.close()
        [checkbox.setCheckable(True) for checkbox in self.main_win.checkboxes]
        self.main_win.moves_made += 1

class Table(QMainWindow):
    def __init__(self, player_index):
        super().__init__()
        self.initUI(0, player_index)

    def initUI(self, p, player_index):
        self.answer = None
        self.moves_made = 0
        self.boxes = []
        self.checkboxes = []
        self.presses = 0
        self.last_throws = (0,0)
        self.figures = []
        self.player_color = QColor(255,255,0)
        self.player_starting_pos = player_index * 14
        self.current_move = 0
        self.player_cnt = 0

        self.command_widget = QVBoxLayout()
        self.roll_dice_button = QPushButton('Roll dice', self)
        self.roll_dice_button.clicked.connect(self._roll_dice)
        self.command_widget.addWidget(self.roll_dice_button)
        self.command_widget.setGeometry(QRect(650,300,200,100))

        #outer parts
        for i in range(0, 7):
            self.__build_square(self.boxes, i, 335, 545-(i % 15)*35, QColor(255, 255, 255))
        for i in range(7, 13):
            self.__build_square(self.boxes, i, 370 + (i - 7)*35, 335, QColor(255,255,255))
        self.__build_square(self.boxes, 13, 545, 300, QColor(255, 255, 255))

        for i in range(14,20):
            self.__build_square(self.boxes, i, 265 + (22 - i)*35,265, QColor(255,255,255))
        for i in range(20,27):
            self.__build_square(self.boxes, i, 335, 265 - (i-20)*35, QColor(255,255,255))
        self.__build_square(self.boxes, 27, 300, 55, QColor(255,255,255))

        for i in range(28,35):
            self.__build_square(self.boxes, i, 265, 55+(i - 28)*35, QColor(255,255,255))
        for i in range(35,41):
            self.__build_square(self.boxes, i, 230 - (i - 35)*35,265, QColor(255,255,255))
        self.__build_square(self.boxes, 41, 55,300, QColor(255,255,255))

        for i in range(42, 49):
            self.__build_square(self.boxes, i, 55 + (i - 42)*35 ,335, QColor(255,255,255))
        for i in range(49,55):
            self.__build_square(self.boxes, i, 265, 370 + (i - 49)*35, QColor(255,255,255))
        self.__build_square(self.boxes, 55,300, 545, QColor(255,255,255))

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

#Table builder function
    def __add_checkbox(self, index):
        box = QVBoxLayout()
        checkbox = QCheckBox(str(index), self)
        self.checkboxes.append(checkbox)
        checkbox.stateChanged.connect(self.signal_for_figure)
        checkbox.setCheckable(False)
        box.addWidget(checkbox)
        self.boxes[index].setLayout(box)

    def __build_square(self, boxes, i, horiz, vert, color):
        self.boxes.append(QFrame(self))
        self.boxes[i].setGeometry(horiz, vert, 30, 30)
        self.boxes[i].setStyleSheet("QWidget {background-color: %s }" % color.name())


# Figure behaviour functions
    def draw_figure(self, figure_pos, player_color, counter):
        self.boxes[figure_pos].setStyleSheet("QWidget {background-color: %s }" % QColor(player_color[0], player_color[1], player_color[2]).name())
        #self.lbl[figure_pos].setText(str(counter))


    def __move_figure(self, old_figure_pos, new_figure_pos):
        #self.__draw_figure(old_figure_pos, (255,255,255))
        #result = function_for_movement()
        #returns tuple like (old_cnt, new_pos, new_cnt)
        old_cnt = 0
        old_pos = old_figure_pos
        new_pos = new_figure_pos
        new_cnt = 1

        if old_cnt:
            self.draw_figure(old_pos, (255,255,255), old_cnt)
        else:
            self.draw_figure(old_pos, (255,255,255), 0)
        self.draw_figure(new_pos, (255,255,0), new_cnt)

    def __get_checked_pos(self):
        i = 0
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                return i
            i += 1

    def signal_for_figure(self):
        #move figure
        old_pos = self.__get_checked_pos()
        self.__move_figure(old_pos, self.current_move)
#######################################
#Dice behaviour functions
    def _roll_dice(self):
        #roll dice
        #server side
        res = testing_event_function()
        self.last_throws = (res['first_dice'], res['second_dice'])
        #checks if a new figure can be used
        if res['can_get_new_figure']:
            for elem in [throw for throw in self.last_throws if throw == 6]:
                self.roll_dice_button.setEnabled(False)
                self.new_window = Popup(self)
            #print(help(self.new_window))
                #backend for choosing the right figure
        return



############################################

    def _get_new_figure(self):
        #backend gets new figure
        #frontend shows new figure
        pass

def testing_event_function():
        first = randrange(1,7)
        second = randrange(1, 7)
        return {'first_dice': 6,
                'second_dice': 6,
                'can_get_new_figure': True if (first == 6 or second == 6) else False}

app = QApplication(sys.argv)
widg = Table(0)
app.exec_()
