import requests
from queue import Queue
import threading
from requests.exceptions import Timeout
import dns.resolver


class SubdomainScanner:
    def __init__(self,domain,tab,bar):
        self.counter = 0
        self.sub_counter = 10
        self.num_lines = 0
        self.tab = tab
        self.bar = bar
        self.tab.insertItem(self.counter, "started")
        self.print_lock = threading.Lock()
        self.domain = domain
        self.q = Queue()
        self.start_threads()
        self.queue_subs()
        self.q.join()
        self.counter +=1
        self.tab.insertItem(self.counter, "Finished")
    
    def test_subdomain(self,sub):
        self.sub_counter+=1
        text = "[" + str(self.sub_counter) + " / " + str(self.num_lines) + "]"
        self.bar.setFormat( text );
        self.bar.setValue(self.sub_counter)

        try:
            url = sub+"."+ self.domain
            ip_dns = dns.resolver.query(url,'A')
            ip = [ip for ip in ip_dns]
            with self.print_lock:
                self.counter+=1
                self.tab.insertItem(self.counter,url + " : " +str(ip))
        except:
            pass

    def queue_subs(self):
        self.num_lines = sum(1 for line in open('data/subdomainstest.dat'))

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
        for _ in range(100):
            t = threading.Thread(target = self.threader)
            t.daemon = True
            t.start()
