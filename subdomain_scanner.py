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


class WorkerSignals(QObject):
    
    progress = pyqtSignal(float,str)
    list     = pyqtSignal(str,int)

class SubdomainScanner(QRunnable):

    def __init__(self,target):
        super(SubdomainScanner, self).__init__()
        self.list_counter   = 0
        self.sub_counter    = 0
        self.wordlist_size  = 0
        self.devnull        = open(os.devnull, 'w')
        self.startTime      = time.time()
        self.signals        = WorkerSignals()
        #self.progress_bar   = progress_bar
        #self.widget_list    = widget_list
        self.print_lock     = threading.Lock()
        self.target         = target
        self.q              = Queue()
    
    
    @pyqtSlot()
    def run(self):
        #self.widget_list.insertItem(self.list_counter, "started")
        self.start_threads()
        self.queue_subs()
        self.q.join()
        #self.widget_list.insertItem(self.list_counter+1, "Finished")


    def test_subdomain(self,sub):

        self.update_bar()
        url = sub+"."+ self.target
        try:
            cevap = subprocess.run(["ping","-c", "1",url],stdout=self.devnull, stderr=self.devnull)
            if cevap.returncode == 0:
                with self.print_lock:
                    #print(url)
                    self.signals.list.emit(url,self.list_counter)
                    self.list_counter+=1
                #self.widget_list.insertItem(self.list_counter,url + " : " +str(ip))
        except:
             #print("except")
             pass


          
    def update_bar(self):
        text = "[" + str(self.sub_counter) + " / " + str(self.wordlist_size) + "]"
        progress_bar_value = (100*self.sub_counter)/(self.wordlist_size)
        #self.progress_bar.setFormat(text);
        #self.progress_bar.setValue(progress_bar_value)
        self.signals.progress.emit(progress_bar_value,text)
        self.sub_counter+=1



    def queue_subs(self):
        self.wordlist_size = sum(1 for line in open('data/subdomains.dat'))

        with open("data/subdomains.dat","r") as fp:
            for line in fp:
                line = line.rstrip("\n")
                self.q.put(line)

    def threader(self):
        while True:
            sub = self.q.get()
            self.test_subdomain(sub)
            self.q.task_done()

    def start_threads(self):
        for _ in range(2):
            t = threading.Thread(target = self.threader)
            t.daemon = True
            t.start()
