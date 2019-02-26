from platform import system as system_name
import datetime
import threading
import queue
import os
import re
import time


def pinger(host, queue):
    param = "-n 1" if system_name().lower() == "windows" else "-c 1"
    result = os.popen("ping " + param + " " + host).read()
    result.encode('cp1251')
    output = str(bytes(result, 'cp1251'), 'cp866')
    regex = re.compile(r".{1,9}?\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}.{1,13}\d{1,3}.{1,7}\d{1,10}.{1,7}\d{1,3}")
    answer = regex.search(output,50)
    logf = open('log.txt', 'a', encoding = 'cp1251')
    time = datetime.datetime.now()
    if ("ttl=" in result.lower()):
        queue.put(answer.group())
        logf.write(time.strftime("%d-%m-%Y %H:%M ") + answer.group() + '\n')
    else:  
        queue.put(host + ' is down!')
        logf.write(time.strftime("%d-%m-%Y %H:%M:%S ") + host + ' is down!\n')
    logf.close()


def worker(queue, filename):
    try:
        file = open(filename, 'r')
    except:
        print('[!] File ' + filename + ' is not found!')
    for line in file:
        host = line.strip()
        if (host[0] == '['):
            continue
        else:
            p = threading.Thread(target=pinger, args=(host, queue,))
            p.start()
            print(queue.get())
        time.sleep(0.5)
    file.close()
    time.sleep(2)


if __name__ == "__main__":
    try:
        queue = queue.Queue()
        while True:
            worker(queue, 'hosts.txt')
    except KeyboardInterrupt:
        print(' [!] Program closed by user!')
    except:
        print('[!] An error has occured, program closed!')