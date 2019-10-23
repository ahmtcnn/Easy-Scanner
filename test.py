from progress.bar import Bar

bar = Bar('Processing', max=20)
for i in range(20):
    # Do some work
    bar.next()
bar.finish()

import os.path
print(os.path.exists('proxy_list.txt'))