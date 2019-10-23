from datetime import datetime
import time

date_format = "%m/%d/%Y"


a = datetime.strptime('8/18/2008', date_format)
b = datetime.strptime('9/26/2008', date_format)
delta = b - a
print delta.days

x = datetime.now()
time.sleep(1)
y = datetime.now()



z = str(x.day)+" "+ str(x.month)

print(z)