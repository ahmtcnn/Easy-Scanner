import asyncio
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import time
import socket


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
    
    result_list     = pyqtSignal(str)
    info_box        = pyqtSignal(str)
    finish_control  = pyqtSignal()


class PortScanner(QRunnable):
    def __init__(self,target):
        super(PortScanner,self).__init__()
        self.target = target
        self.signals = WorkerSignals()
        self.start_time = time.time()


    @pyqtSlot()
    def run(self):
        view = "Port\tService"
        self.signals.result_list.emit(view)
        loop = asyncio.new_event_loop()
        self.result = loop.run_until_complete(run(self.target))
        self.print_result()
        later = time.time()
        time_taken = later - self.start_time
        self.signals.info_box.emit("[✔] Port Scan finished!")
        self.signals.info_box.emit("Time taken: %.2f seconds" % time_taken)
        self.signals.finish_control.emit()

    def print_result(self):

        for port in self.result:
            if port != None:
                try:
                    service= socket.getservbyport(port)
                except:
                    service = "unknown"
                    print(port)
                port_text = str(port)+"\t"+service
                self.signals.result_list.emit(port_text)









