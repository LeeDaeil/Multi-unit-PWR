import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Function_Mem_ShMem import InterfaceMem
from Interface_ABCWidget import *
from Interface_QSS import qss

from Interface_MainTopBar import MainTopBar
from Interface_CNS import CNSController

class Main(QWidget):
    def __init__(self, ShMems):
        super(Main, self).__init__()
        self.inmem:InterfaceMem = InterfaceMem(ShMems, self)
        self.setGeometry(0, 0, 1024, 768)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 상단바 제거
        self.setObjectName('Main')
        self.setStyleSheet(qss) # qss load
        self.m_flag = False
        # Frame ------------------------------------------------------
        gl = QGridLayout(self)
        self.maintopbar = MainTopBar(self)
        
        gl.addWidget(self.maintopbar, 0, 0, 1, 2)
        gl.addWidget(UnitWidget(self, 0), 1, 0, 1, 1)
        gl.addWidget(UnitWidget(self, 1), 2, 0, 1, 1)
        gl.addWidget(UnitWidget(self, 2), 1, 1, 1, 1)
        gl.addWidget(UnitWidget(self, 3), 2, 1, 1, 1)

        # End frame --------------------------------------------------
        self.CNSController = CNSController(self)

    # window drag
    def mousePressEvent(self, event):        
        if (event.button() == Qt.LeftButton) and self.maintopbar.check_mouse_in_area():
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag and self.maintopbar.check_mouse_in_area():
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 윈도우 position 변경
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def close(self) -> bool:
        QApplication.closeAllWindows()
        return super().close()
class UnitWidget(ABCWidget):
    def __init__(self, parent, unit, widget_name=''):
        super().__init__(parent, widget_name)
        vl = QVBoxLayout(self)
        vl.addWidget(UnitTitleLabel(self, unit))
        hl = QHBoxLayout()
        hl.addWidget(UnitLabel(self, unit, 'Power', 'KBCDO23', '[%]'))
        hl.addWidget(UnitLabel(self, unit, 'Electric Power', 'KBCDO22', '[MWe]'))
        vl.addLayout(hl)
        hl2 = QHBoxLayout()
        hl2.addWidget(UnitStateNormal(self, unit))
        hl2.addWidget(UnitStateAbnormal(self, unit))
        hl2.addWidget(UnitStateEmergency(self, unit))
        vl.addLayout(hl2)
class UnitTitleLabel(ABCLabel):
    def __init__(self, parent, unit, widget_name=''):
        super().__init__(parent, widget_name)
        self.setText(f'Module {unit + 1}')
        self.setFixedHeight(40)
class UnitLabel(ABCLabel):
    def __init__(self, parent, unit, title, para, scale, widget_name=''):
        super().__init__(parent, widget_name)
        self.para = para
        self.scale = scale
        self.unit = unit
        self.title = title
        self.startTimer(600)
        
    def timerEvent(self, a0: 'QTimerEvent') -> None:
        self.setText(f'{self.title}\n{self.inmem.get_para_val(self.unit, self.para)} {self.scale}')
        return super().timerEvent(a0)
class UnitStateNormal(ABCLabel):
    def __init__(self, parent, unit, widget_name=''):
        super().__init__(parent, widget_name)
        self.setProperty('State', 'Off')
        self.setText('Normal')
        self.unit = unit
        self.startTimer(600)
        
    def timerEvent(self, a0: 'QTimerEvent') -> None:
        self.setProperty('State', 'On' if 95 <= self.inmem.get_para_val(self.unit, 'KBCDO23') else 'Off')
        self.style().polish(self)
        return super().timerEvent(a0)
class UnitStateAbnormal(ABCLabel):
    def __init__(self, parent, unit, widget_name=''):
        super().__init__(parent, widget_name)
        self.setProperty('State', 'Off')
        self.setText('Abnormal')
        self.unit = unit
        self.startTimer(600)
        
    def timerEvent(self, a0: 'QTimerEvent') -> None:
        self.setProperty('State', 'On' if 10 < self.inmem.get_para_val(self.unit, 'KBCDO23') < 95 else 'Off')
        self.style().polish(self)
        return super().timerEvent(a0)
class UnitStateEmergency(ABCLabel):
    def __init__(self, parent, unit, widget_name=''):
        super().__init__(parent, widget_name)
        self.setProperty('State', 'Off')
        self.setText('Emergency')
        self.unit = unit
        self.startTimer(600)
        
    def timerEvent(self, a0: 'QTimerEvent') -> None:
        self.setProperty('State', 'On' if self.inmem.get_para_val(self.unit, 'KBCDO23') <= 10 else 'Off')
        self.style().polish(self)
        return super().timerEvent(a0)