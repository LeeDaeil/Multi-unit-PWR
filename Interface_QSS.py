# ref : https://het.as.utexas.edu/HET/Software/html/stylesheet-reference.html
# ref : https://doc.qt.io/archives/qt-4.8/stylesheet-examples.html#customizing-qgroupbox
# ref : https://wikidocs.net/book/2957
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# Qss builder -------------------------------------------------
def builder(objecttype:str, objectname:str, contents:list):
    qss_info = f'{objecttype}#{objectname}' + '{'
    
    for content in contents:
        qss_info += f'{content};'
    
    qss_info += '}'
    
    return qss_info
def rgb_to_qCOLOR(color_code:str):
    color_code = color_code.replace('rgb(', '').replace(')', '').replace(' ', '').split(',')
    return QColor(int(color_code[0]), int(color_code[1]), int(color_code[2]))

# Color Table -------------------------------------------------
DarkGray = 'rgb(80, 80, 80)'
Gray = 'rgb(181, 181, 181)'
LightGray = 'rgb(231, 231, 234)'
LightWhite = 'rgb(255, 255, 255)'
LightBlue = 'rgb(0, 178, 216)'
DarkRed = 'rgb(192, 0, 0)'
Yellow = 'rgb(249, 249, 0)'
DarkYellow = 'rgb(255, 192, 0)'
Black = 'rgb(0, 0, 0)'
Green = 'rgb(0, 170, 0)'
Orange = 'rgb(255, 192, 0)'
# Font Table --------------------------------------------------
Global_font_size_nub = 20
Content_font_size_nub = 15
Mimic_font_size_nub = 12
Global_font_size = f'{Global_font_size_nub}pt'
Content_font_size = f'{Content_font_size_nub}pt'
Global_font = 'Arial'
Global_font2 = '맑은 고딕'

# Qss ---------------------------------------------------------
QssMain = ''.join([
    builder('QWidget', 'Main', [f'background-color: {DarkGray};']),
    # Interface_MainTopBar.py ------------------------------------------------------------------------
    builder('QWidget', 'MainTopBar', [f'background-color: {DarkGray};', 'border-radius: 5px;']),
    builder('QLabel', 'MainTopBarTimer', [f'background-color: {LightGray};', f'font-family: {Global_font};', f'font-size: {Global_font_size};', "qproperty-alignment: 'AlignCenter';", 'border-radius: 5px;']),
    builder('QPushButton', 'MainTopBarClose', [f'border-image: url(Img/close.png);','border-radius: 5px;']),
    # Interface_Main.py ------------------------------------------------------------------------------
    builder('QWidget', 'UnitWidget', [f'background-color: {Gray};', 'border-radius: 5px;']),
    builder('QLabel', 'UnitTitleLabel', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};', "qproperty-alignment: 'AlignCenter';", 'font-weight: bold;']),
    builder('QLabel', 'UnitLabel', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Global_font_size};', "qproperty-alignment: 'AlignCenter';", 'font-weight: bold;']),
    builder('QLabel', 'UnitStateNormal', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', "qproperty-alignment: 'AlignCenter';", 'font-weight: bold;']),
    builder('QLabel', 'UnitStateNormal[State="On"]', [f'background-color: {Green};']),
    builder('QLabel', 'UnitStateNormal[State="Off"]', [f'background-color: {LightGray};']),
    builder('QLabel', 'UnitStateAbnormal', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', "qproperty-alignment: 'AlignCenter';", 'font-weight: bold;']),
    builder('QLabel', 'UnitStateAbnormal[State="On"]', [f'background-color: {DarkYellow};']),
    builder('QLabel', 'UnitStateAbnormal[State="Off"]', [f'background-color: {LightGray};']),
    builder('QLabel', 'UnitStateEmergency', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', "qproperty-alignment: 'AlignCenter';", 'font-weight: bold;']),
    builder('QLabel', 'UnitStateEmergency[State="On"]', [f'background-color: {DarkRed};']),
    builder('QLabel', 'UnitStateEmergency[State="Off"]', [f'background-color: {LightGray};']),
    # Interface_CNS.py -------------------------------------------------------------------------------
    builder('QWidget', 'CNSController', [f'background-color: {Gray};', 'border-radius: 5px;']),
    builder('QLabel', 'CNSControllerTitle', [f'background-color: {LightBlue};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', "qproperty-alignment: 'AlignCenter';", 'font-weight: bold;']),
    builder('QPushButton', 'CNSControllerInit', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'font-weight: bold;']),
    builder('QPushButton', 'CNSControllerRun', [f'background-color: {LightWhite};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'font-weight: bold;']),
    builder('QPushButton', 'CNSControllerMal', [f'background-color: {Green};', 'border-radius: 5px;', f'font-family: {Global_font};', f'font-size: {Content_font_size};', 'font-weight: bold;']),
])
# final qss !! 
qss = ''.join(
    [QssMain]
)