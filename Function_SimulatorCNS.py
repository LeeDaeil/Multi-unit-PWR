import multiprocessing
import time
from Function_Mem_ShMem import ShMem
from TOOL.TOOL_CNS_UDP_FAST import CNS

class WrapCNS(multiprocessing.Process):
    def __init__(self, nub, mem, cns_ip, cns_port, com_ip, com_port) -> None:
        super(WrapCNS, self).__init__()
        self.daemon = True
        self.update_interval = 1
        self.nub = nub
        self.mem:ShMem = mem
        
        self.CNS = CNS(f'Unit{nub}', cns_ip, cns_port, com_ip, com_port, Max_len=2)
        self.CNS.init_cns(1)
        
    def mapping_mem(self):
        [self.mem.change_para_val(para, self.CNS.mem[para]['Val']) for para in self.CNS.mem.keys()]
    
    def run(self) -> None:
        while True:
            if self.mem.get_logic('Run'):
                self.mapping_mem()
                self.CNS.run_freeze_CNS()
                time.sleep(self.update_interval)
            else:
                if self.mem.get_logic('Init_Call'):
                    print('Call init')
                    self.CNS.init_cns(1)
                    self.mem.change_logic('Init_Call', False)
                if self.mem.get_logic('Mal_LOCA_Call'):
                    print('Activate LOCA')
                    self.CNS._send_malfunction_signal(12, 100100, 10)
                    self.mem.change_logic('Mal_LOCA_Call', False)
                if self.mem.get_logic('Mal_Rod_Call'):
                    print('Activate Rod')
                    self.CNS._send_malfunction_signal(2, 123, 10)
                    self.mem.change_logic('Mal_Rod_Call', False)