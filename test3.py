import asyncio
import socket
import threading
import time
from queue import Queue
import socket
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class WorkerSignals(QObject):
    
    progress = pyqtSignal(float,str)
    list     = pyqtSignal(str,int)

class PortScanner(QRunnable):
    def __init__(self,target):
        super(PortScanner, self).__init__()
        self.target = target
        print(target)

    @pyqtSlot()
    def run(self):
        print("debug1")
        #loop = asyncio.get_event_loop()
        #future = asyncio.ensure_future(start())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start())
        print('#'*50)


    async def check_port(self,port):
        print("debug2")
        conn = asyncio.open_connection(self.target, port)
        try:
            reader, writer = await asyncio.wait_for(conn, timeout=3)
            print(port, 'ok')
        except:
            pass
        finally:
            if 'writer' in locals():
                writer.close()

    async def check_port_sem(self,sem,port):
        async with sem:
            return await self.check_port(port)

    async def start(self):
        print("debug2")
        sem = asyncio.Semaphore(600) #Change this value for concurrency limitation
        tasks = []

        for port in range(65500):
            task = asyncio.ensure_future(self.check_port_sem(sem,port))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

