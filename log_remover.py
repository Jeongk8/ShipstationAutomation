
import os
from random import randint




def move():
    dap = dict() 
    for x in os.listdir("C:\\Library\\workspace\\ship_world"):
        if x[-4:] == ".txt":
            dap["C:\\Library\\workspace\\ship_world\\"+str(x)] = os.path.getmtime("C:\\Library\\workspace\\ship_world\\"+str(x))
    
    dap = {k:v for k,v in sorted(dap.items(), key = lambda x: -x[1])}
    final=''
    for k,x in dap.items():
        final = k
        break
        
    os.rename(final,"C:\\Library\\ship_work_log\\"+str(randint(1000,10000000))+".txt")




move()
