import requests
from queue import Queue
import threading
from requests.exceptions import Timeout


class SubdomainScanner:
    def __init__(self,domain):
        self.OKGREEN = '\033[92m'
        self.ENDC = '\033[0m'
        self.WARNING = '\033[91m'
        self.TIMEOUT = '\033[95m'
        self.print_lock = threading.Lock()
        self.domain = domain
        self.q = Queue()
        self.start_threads()
        self.queue_subs()
        self.q.join()
        print("finished")
    
    def test_subdomain(self,sub):
        try:
            url = "http://"+sub+"."+ self.domain
            response = requests.get(url,timeout=(6,12))
            with self.print_lock:
                print(self.OKGREEN + url + " : " +str(response.status_code)+ self.ENDC)
        except Timeout:
            try:
                url = "http://"+sub+"."+ self.domain
                response = requests.get(url,timeout=(10,15))
                with self.print_lock:
                    print(self.OKGREEN + url + " : " +str(response.status_code)+ self.ENDC)
            except:
                pass
        except:
            pass

    def queue_subs(self):
        with open("subdomains.dat","r") as fp:
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

    def test(self,url):
        url = "http://"+ url
        response = requests.get(url,timeout=(5,12))
        with self.print_lock:
            print(self.OKGREEN + url + " : " +str(response.status_code)+ self.ENDC)


scanner = SubdomainScanner("instra.com")


# import requests
# from queue import Queue
# import threading
# from requests.exceptions import Timeout


# class SubdomainScanner:
#     def __init__(self,domain):
#         self.OKGREEN = '\033[92m'
#         self.ENDC = '\033[0m'
#         self.WARNING = '\033[91m'
#         self.TIMEOUT = '\033[95m'
#         self.print_lock = threading.Lock()
#         self.domain = domain
#         self.q = Queue()
#         self.start_threads()
#         self.queue_subs()
#         self.q.join()
#         print("finished")
    
#     def test_subdomain(self,sub):
#         try:
#             url = "http://"+sub+"."+ self.domain
#             response = requests.get(url,timeout=(6,12))
#             with self.print_lock:
#                 print(self.OKGREEN + url + " : " +str(response.status_code)+ self.ENDC)
#         except Timeout:
#             try:
#                 url = "http://"+sub+"."+ self.domain
#                 response = requests.get(url,timeout=(10,15))
#                 with self.print_lock:
#                     print(self.OKGREEN + url + " : " +str(response.status_code)+ self.ENDC)
#             except:
#                 pass
#         except:
#             pass

#     def queue_subs(self):
#         with open("subdomains.dat","r") as fp:
#             for line in fp:
#                 line = line.rstrip("\n")
#                 self.q.put(line)

#     def threader(self):
#         while True:
#             sub = self.q.get()
#             self.test_subdomain(sub)
#             self.q.task_done()

#     def start_threads(self):
#         for _ in range(100):
#             t = threading.Thread(target = self.threader)
#             t.daemon = True
#             t.start()

#     def test(self,url):
#         url = "http://"+ url
#         response = requests.get(url,timeout=(5,12))
#         with self.print_lock:
#             print(self.OKGREEN + url + " : " +str(response.status_code)+ self.ENDC)


# scanner = SubdomainScanner("instra.com")