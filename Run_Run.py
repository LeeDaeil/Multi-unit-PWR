"""

Run_Run

"""

from multiprocessing.managers import BaseManager
from multiprocessing import Process
import sys
from PyQt5.QtWidgets import *

from Function_Mem_ShMem import ShMem
from Function_SimulatorCNS import WrapCNS
from Interface_Main import Main


class Run:
    def __init__(self):
        pass

    def make_shmem(self):
        BaseManager.register('ShMem', ShMem)
        manager = BaseManager()
        manager.start()
        mem = manager.ShMem()
        return mem

    def start_process(self):
        """ MainProcess 동작 """
        mem1 = self.make_shmem()
        mem2 = self.make_shmem()
        mem3 = self.make_shmem()
        mem4 = self.make_shmem()
        cns_ip = '192.168.0.6'
        cns_port = 7100
        com_ip = '192.168.0.12'
        p_list = [InterfaceRun([mem1, mem2, mem3, mem4]), 
                  WrapCNS(0, mem1, cns_ip, cns_port + 1, com_ip, cns_port + 1),  
                  WrapCNS(1, mem2, cns_ip, cns_port + 2, com_ip, cns_port + 2), 
                  WrapCNS(2, mem3, cns_ip, cns_port + 3, com_ip, cns_port + 3), 
                  WrapCNS(3, mem4, cns_ip, cns_port + 4, com_ip, cns_port + 4)]
        [pr_.start() for pr_ in p_list]
        [pr_.join() for pr_ in p_list]  # finished at the same time

class InterfaceRun(Process):
    def __init__(self, mems):
        super(InterfaceRun, self).__init__()
        self.mems = mems
    
    def run(self) -> None:
        app = QApplication(sys.argv)
        app.setStyle('Windows')
        w = Main(self.mems)
        w.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    MainProcess = Run()
    MainProcess.start_process()
