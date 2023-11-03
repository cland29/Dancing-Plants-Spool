from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import time

class Position_Selector(QWidget):
    def __init__(self, min_pos, max_pos, step_size, pos_update_func):
        super(Position_Selector, self).__init__()

        self.cur_pos = 0
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.step_size = step_size
        self.initUI()
        self.pos_update_func = pos_update_func

    def initUI(self):
        vert_layout = QVBoxLayout()
        hor_layout = QHBoxLayout()

        self.value_widget = QSpinBox()
        self.value_widget.setMinimum(self.min_pos)
        self.value_widget.setMaximum(self.max_pos)
        self.value_widget.setSingleStep(self.step_size)
        self.value_widget.valueChanged.connect(self.change_pos)

        label = QLabel("Check for Live Update:")

        self.live_update_widget = QCheckBox()
        self.live_update_widget.setCheckState(Qt.CheckState.Unchecked)
        self.live_update_widget.stateChanged.connect(self.set_cur_pos)

        hor_layout.addWidget(self.value_widget)
        hor_layout.addWidget(label)
        hor_layout.addWidget(self.live_update_widget)

        self.slider_widget = QSlider(Qt.Orientation.Horizontal)
        self.slider_widget.setMinimum(self.min_pos)
        self.slider_widget.setMaximum(self.max_pos)
        self.slider_widget.valueChanged.connect(self.change_pos)

        vert_layout.addLayout(hor_layout)
        vert_layout.addWidget(self.slider_widget)

        #full_widget = QWidget()
        self.setLayout(vert_layout)

    def change_pos(self, new_pos):
        self.cur_pos = new_pos
        self.slider_widget.setValue(self.cur_pos)
        self.value_widget.setValue(self.cur_pos)

        self.set_cur_pos()

    def set_cur_pos(self):
        if (self.live_update_widget.checkState() == Qt.CheckState.Checked):
            self.pos_update_func(self.cur_pos)





class ControllerWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ControllerWindow, self).__init__(*args, **kwargs)
        self.pos1 = 0
        self.pos2 = 0
        self.pos3 = 0
        self.initUI()

    def initUI(self):
            self.setWindowTitle("my window")
            self.num = 2


            self.pos_list = QListWidget()
            self.pos_list.addItems(["one", "1,3,4", "3,5,6"])
            self.pos_list.currentItemChanged.connect(self.set_position_values)




            # creating a button to be clicked
            #button1 = QPushButton('Button-1', self)
            #        button1.move(100, 70)
            #button1.clicked.connect(self.on_click)

            top_layout = QHBoxLayout()
            top_layout.addWidget(Position_Selector(0, 100, 2, self.set_pos1))
            top_layout.addWidget(Position_Selector(0, 100, 2, self.set_pos2))
            top_layout.addWidget(Position_Selector(0, 100, 2, self.set_pos3))


            self.layout = QVBoxLayout(self)

            #self.layout.addWidget(button1)
            self.layout.addLayout(top_layout)

            testButton = QPushButton()
            testButton.setText("Save Position")
            testButton.pressed.connect(self.sav_full_pos)
            self.layout.addWidget(testButton)

            self.layout.addWidget(self.pos_list)




            widget = QWidget()
            widget.setLayout(self.layout)

            self.setCentralWidget(widget)

    @pyqtSlot()
    def on_click(self):
            print('Button-{} will be created'.format(self.num))
            button2 = QPushButton('Button-{}'.format(self.num), self)
            button2.clicked.connect(lambda: print(button2.text()))

            button2.move(0, 30 * (self.num - 1))
            button2.show()

            self.layout.addWidget(button2)
            self.num += 1

    def set_position_values(self, passed_val):
        print(passed_val.text())
        setpoint_val = passed_val.text().split(",")
        if(len(setpoint_val) == 3 and setpoint_val[0].isnumeric() and setpoint_val[1].isnumeric() and setpoint_val[2].isnumeric()):
            self.pos1 = int(setpoint_val[0])
            self.pos2 = int(setpoint_val[1])
            self.pos3 = int(setpoint_val[2])
        else:
            print("Not numeric Inputs of list 3")
        print("Positions changed to:",self.pos1, self.pos2, self.pos3)

    def set_pos1(self, update_pos):
        self.pos1 = update_pos

    def set_pos2(self, update_pos):
        self.pos2 = update_pos

    def set_pos3(self, update_pos):
        self.pos3 = update_pos

    def sav_full_pos(self):
        self.pos_list.addItem(f"{self.pos1},{self.pos2},{self.pos3}")



if __name__ == "__main__":
    app = QApplication([])

    window = ControllerWindow()
    window.show()

    app.exec()