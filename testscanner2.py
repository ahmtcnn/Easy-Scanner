import socket
import time
import threading
from queue import Queue       
    
socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()

target = '176.53.35.152'

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target, port))
        with print_lock:
            print('Port', port, 'is open!')
        con.close()
    except:
        pass

def threader():
    while True:
        port = q.get()
        portscan(port)
        q.task_done()

q = Queue()
startTime = time.time()


for port in range(1, 65536):
    q.put(port)

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()



q.join()

print('Time taken:', time.time() - startTime)