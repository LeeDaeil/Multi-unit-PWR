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
        
        self.trig = False
        
    def mapping_mem(self):
        [self.mem.change_para_val(para, self.CNS.mem[para]['Val']) for para in self.CNS.mem.keys()]
    
    def run(self) -> None:
        while True:
            self.mapping_mem()
            self.CNS.run_freeze_CNS()
            
            if self.nub == 0 and not self.trig:
                self.CNS._send_malfunction_signal(12, 100100, 10)
                self.trig = True
            
            time.sleep(self.update_interval)