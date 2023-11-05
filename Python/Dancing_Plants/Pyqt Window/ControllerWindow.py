from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import time

class Position_Selector(QWidget):
    def __init__(self, min_pos, max_pos, step_size):
        super(Position_Selector, self).__init__()


        self.min_pos = min_pos
        self.max_pos = max_pos
        self.step_size = step_size
        self.initUI()


    def initUI(self):
        vert_layout = QVBoxLayout()
        hor_layout = QHBoxLayout()

        self.value_widget = QSpinBox()
        self.value_widget.setMinimum(self.min_pos)
        self.value_widget.setMaximum(self.max_pos)
        self.value_widget.setSingleStep(self.step_size)
        self.value_widget.valueChanged.connect(self.change_pos)



        self.slider_widget = QSlider(Qt.Orientation.Horizontal)
        self.slider_widget.setMinimum(self.min_pos)
        self.slider_widget.setMaximum(self.max_pos)
        self.slider_widget.valueChanged.connect(self.change_pos)

        vert_layout.addWidget(self.value_widget)
        vert_layout.addWidget(self.slider_widget)


        self.setLayout(vert_layout)

    def change_pos(self, new_pos):
        self.slider_widget.setValue(new_pos)
        self.value_widget.setValue(new_pos)

    def get_pos(self):
        return self.value_widget.value()










class ControllerWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ControllerWindow, self).__init__(*args, **kwargs)
        self.pos_sel_widgets = []
        self.initUI()

    def initUI(self):
            self.setWindowTitle("my window")
            self.num = 2

            top_layout = QHBoxLayout()

            for i in range(3):
                self.pos_sel_widgets.append(Position_Selector(0, 100, 2))
                top_layout.addWidget(self.pos_sel_widgets[i])




            self.pos_list = QListWidget()
            self.pos_list.addItems([])
            self.pos_list.currentItemChanged.connect(self.set_position_values)


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


    def set_position_values(self, passed_val):
        print(passed_val.text())
        setpoint_val = passed_val.text().split(",")
        print(setpoint_val)

        for i in range(len(self.pos_sel_widgets)):
            self.pos_sel_widgets[i].change_pos(int(setpoint_val[i]))



    def sav_full_pos(self):
        #Did it this way so that you would have comma's in between values but not at the very end
        pos = ""
        for i in range(len(self.pos_sel_widgets) - 1):
            pos = pos + str(self.pos_sel_widgets[i].get_pos()) + ","
        pos = pos + str(self.pos_sel_widgets[-1].get_pos())

        self.pos_list.addItem(pos)



if __name__ == "__main__":
    app = QApplication([])

    window = ControllerWindow()
    window.show()

    app.exec()