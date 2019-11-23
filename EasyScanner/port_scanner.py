import asyncio
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


async def check_port(target,port):
    conn = asyncio.open_connection(target, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=3)
        return port
    except:
        pass
    finally:
        if 'writer' in locals():
            writer.close()

async def check_port_sem(sem,target,port):
    async with sem:
        return await check_port(target,port)

async def run(target):
    sem = asyncio.Semaphore(600) #Change this value for concurrency limitation
    tasks = []

    for port in range(3000):
        task = asyncio.ensure_future(check_port_sem(sem,target,port))
        tasks.append(task)
    responses = await asyncio.gather(*tasks)
    return responses


class WorkerSignals(QObject):
    
    #progress = pyqtSignal(float,str)
    port_list     = pyqtSignal(str)
    info_list = pyqtSignal(str)


class PortScanner(QRunnable):
    def __init__(self,target):
        super(PortScanner,self).__init__()
        self.target = target
        self.signals = WorkerSignals()


    @pyqtSlot()
    def run(self):
        start_text = "[✔] Port Scan Started"
        view = "Port\tService"
        self.signals.port_list.emit(start_text)
        self.signals.port_list.emit(view)
        loop = asyncio.new_event_loop()
        self.result = loop.run_until_complete(run(self.target))
        self.print_result()

    def print_result(self):

        for port in self.result:
            if port != None:
                try:
                    service= socket.getservbyport(port)
                except:
                    service = "unknown"
                port_text = str(port)+"\t"+service
                self.signals.port_list.emit(port_text)

        stop_text = "[✔] Port Scan Finished"
        self.signals.port_list.emit(stop_text)







