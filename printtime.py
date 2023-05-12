import time
print('time.time()')
start = time.time()
while True:
    end = time.time()
    print(end - start, 's')
    time.sleep(5)