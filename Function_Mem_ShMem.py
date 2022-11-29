from datetime import timedelta
from Function_Mem_AlarmDB import AlarmDB
from collections import deque
import pandas as pd

class ShMem:
    def __init__(self):
        self.mem = self.make_cns_mem(max_len=10)
        self.AlarmDB: AlarmDB = AlarmDB(self)
        self.add_val_to_list()
        self.logic = {'Run': False, 'Init_Call':False, 'Init_nub': 1, 'Mal_Call': False, 'Mal_list': {}}

    def make_cns_mem(self, max_len, db_path='./db.txt', db_add_path='./db_add.txt'):
        # 초기 shared_mem의 구조를 선언한다.
        idx = 0
        shared_mem = {}
        for file_name in [db_path, db_add_path]:
            with open(file_name, 'r') as f:
                while True:
                    temp_ = f.readline().split('\t')
                    if temp_[0] == '':  # if empty space -> break
                        break
                    if temp_[0] == '#':  # Pass this value. We don't require this value.
                        pass  # These values are normally static values in SMABRES Code.
                    else:
                        sig = 0 if temp_[1] == 'INTEGER' else 1
                        shared_mem[temp_[0]] = {'Sig': sig, 'Val': 0, 'Num': idx, 'List': deque(maxlen=max_len)}
                        idx += 1

        # 다음과정을 통하여 shared_mem 은 PID : { type. val, num }를 가진다.
        return shared_mem

    def update_alarmdb(self):
        self.AlarmDB.update_alarmdb_from_ShMem()

    def add_val_to_list(self):
        [self.mem[para]['List'].append(self.mem[para]['Val']) for para in self.mem.keys()]

    def change_para_val(self, para, val):
        self.mem[para]['Val'] = val
    
    def change_mal_val(self, mal_index, mal_dict):
        self.logic['Mal_list'][mal_index] = mal_dict
        self.logic['Mal_Call'] = True
        
    def get_para_val(self, para):
        return self.mem[para]['Val']

    def get_para_list(self, para):
        return self.mem[para]['List']

    def get_alarmdb(self):
        return self.AlarmDB.alarmdb
        
    def get_on_alarms(self):
        return self.AlarmDB.get_on_alarms()

    def get_on_alarms_des(self):
        return self.AlarmDB.get_on_alarms_des()

    def get_alarm_des(self, para):
        return self.AlarmDB.get_alarm_des(para)
    
    def get_alarm_para(self, type_):
        return self.AlarmDB.get_alarm_para(type_)

    def check_para_name(self, para):
        return True if para in self.mem.keys() else False

    def check_para_type(self, para):
        return self.mem[para]['Sig']

    def call_run(self):
        self.logic['Run'] = True
    
    def call_freeze(self):
        self.logic['Run'] = False
    
    def call_init(self):
        self.logic['Init_Call'] = True
    
    def call_mal(self):
        self.logic['Mal_Call'] = True
    
    def get_logic(self, para):
        return self.logic[para]
    
    def change_logic(self, para, val):
        self.logic[para] = val

class InterfaceMem:
    def __init__(self, Shmems, top_widget):
        self.ShMemUnits = {unit_nub:mem for unit_nub, mem in enumerate(Shmems)}
        self.widget_ids = {}
        # Top_widget 정보 등록
        self.add_widget_id(top_widget)

    # Widget 링크 용 ----------------------------------------------------------------------------------------------------
    def add_widget_id(self, widget, widget_name=''):
        """새롭게 생성된 위젯의 정보를 self.widget_ids:dict 에 저장하는 함수

        Args:
            widget (_type_): Qwidget, QPushButton를 기반한 ABC 클래스
            widget_name (str, optional): 클래스의 이름이 중복적으로 사용되는 경우 수동 할당을 위해서 존재. Defaults to '' 는 class 명을 따라감.
        """
        self.widget_ids[type(widget).__name__ if widget_name == '' else widget_name] = widget

    def show_widget_ids(self):
        return self.widget_ids

    def get_time(self):
        return str(timedelta(seconds=self.ShMemUnits[0].get_para_val('KCNTOMS') / 5))

    def get_para_val(self, unit, para):
        return self.ShMemUnits[unit].get_para_val(para)

    def call_init(self):
        [self.ShMemUnits[unit].call_init() for unit in self.ShMemUnits.keys()]

    def call_run(self):
        [self.ShMemUnits[unit].call_run() for unit in self.ShMemUnits.keys()]
    
    def call_freeze(self):
        [self.ShMemUnits[unit].call_freeze() for unit in self.ShMemUnits.keys()]
        
    def call_mal(self, unit):
        self.ShMemUnits[unit].call_mal()