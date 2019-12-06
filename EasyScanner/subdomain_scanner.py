import requests
from queue import Queue
import threading
from requests.exceptions import Timeout
import dns.resolver
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
from scapy.all import *
import subprocess
import time

class WorkerSignals(QObject):
    
    result_list     = pyqtSignal(str)
    info_box        = pyqtSignal(str)
    finish_control  = pyqtSignal()

class SubdomainScanner(QRunnable):

    def __init__(self,target):
        super(SubdomainScanner,self).__init__()
        self.list_counter   = 0
        self.sub_counter    = 0
        self.wordlist_size  = 0
        self.devnull        = open(os.devnull, 'w')
        self.startTime      = time.time()
        self.signals        = WorkerSignals()
        self.target         = target
        self.q              = Queue()
    
    
    @pyqtSlot()
    def run(self):
        starter = time.time()
        self.start_threads()
        self.queue_subs()
        self.q.join()
        print("finished")
        finish = time.time()
        self.signals.finish_control.emit()
        difference = finish - starter
        self.signals.info_box.emit("Time Taken: "+str(difference))


    def test_subdomain(self,sub):

        url = sub+"."+ self.target
        try:
            cevap = subprocess.run(["ping","-c", "1",url],stdout=self.devnull, stderr=self.devnull)
            if cevap.returncode == 0:
                self.signals.result_list.emit(url)
        except:
             pass



    def queue_subs(self):
        self.wordlist_size = sum(1 for line in open('data/subdomainstest.dat'))

        with open("data/subdomainstest.dat","r") as fp:
            for line in fp:
                line = line.rstrip("\n")
                self.q.put(line)

    def threader(self):
        while True:
            sub = self.q.get()
            self.test_subdomain(sub)
            self.q.task_done()

    def start_threads(self):
        for _ in range(10):
            t = threading.Thread(target = self.threader)
            t.daemon = True
            t.start()
