import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Function_Mem_ShMem import InterfaceMem
from Interface_ABCWidget import *
from Interface_QSS import qss

class CNSController(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setStyleSheet(qss)
        self.setGeometry(0, 0, 200, 200)
        vl = QVBoxLayout(self)
        vl.addWidget(CNSControllerTitle(self))
        vl.addWidget(CNSControllerInit(self))
        vl.addWidget(CNSControllerRun(self))
        gl = QGridLayout()
        gl.addWidget(CNSControllerMalLoca(self, 0), 0, 0, 1, 1)
        gl.addWidget(CNSControllerMalRod(self,  0), 1, 0, 1, 1)
        gl.addWidget(CNSControllerMalLoca(self, 1), 2, 0, 1, 1)
        gl.addWidget(CNSControllerMalRod(self,  1), 3, 0, 1, 1)
        gl.addWidget(CNSControllerMalLoca(self, 2), 0, 1, 1, 1)
        gl.addWidget(CNSControllerMalRod(self,  2), 1, 1, 1, 1)
        gl.addWidget(CNSControllerMalLoca(self, 3), 2, 1, 1, 1)
        gl.addWidget(CNSControllerMalRod(self,  3), 3, 1, 1, 1)
        vl.addLayout(gl)
class CNSControllerTitle(ABCLabel):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('CNS Controller')
        self.setFixedHeight(40)
class CNSControllerInit(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Call Init')
    
    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.inmem.call_init()
        return super().mousePressEvent(e)
class CNSControllerRun(ABCPushButton):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText('Freeze')
        self.Condition = False
    
    def mousePressEvent(self, e: QMouseEvent) -> None:
        if self.Condition:
            self.inmem.call_freeze()
            self.setText('Freeze')
            self.Condition = False
        else:
            self.inmem.call_run()
            self.setText('Run')
            self.Condition = True
        return super().mousePressEvent(e)
class CNSControllerMalLoca(ABCPushButton):
    def __init__(self, parent, unit, widget_name=''):
        super().__init__(parent, widget_name)
        self.unit = unit
        self.setText(f'Mal LOCA\nModule {unit}')
        self.Condition = False
    
    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.inmem.call_mal_loca(self.unit)
        self.setText('Activate')
        return super().mousePressEvent(e)
class CNSControllerMalRod(ABCPushButton):
    def __init__(self, parent, unit, widget_name=''):
        super().__init__(parent, widget_name)
        self.unit = unit
        self.setText(f'Mal Rod\nModule {unit}')
        self.Condition = False
    
    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.inmem.call_mal_rod(self.unit)
        self.setText('Activate')
        return super().mousePressEvent(e)