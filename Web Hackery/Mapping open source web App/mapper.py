import contextlib
import os
import queue
import requests
import sys
import threading
import time

FILTERED = [".jpg",".gif",".png",".css",".scss",".svg"]
THREADS = 10
GREEN = '\033[92m'  
RESET = '\033[0m'

answers = queue.Queue()
web_paths = queue.Queue()

def gather_paths():
    for root,_,files in os.walk('.'):
        for fname in files :
            if os.path.splitext(fname)[1] in FILTERED :
                continue
            path = os.path.join(root,fname)
            if path.startswith('.'):
                path = path[1:]
            #print(path)
            web_paths.put(path)

@contextlib.contextmanager
def chdir(path):
  """
    On enter, change  directory to specified path
    On exit, change directory back to original
  """
  this_dir = os.getcwd()
  os.chdir(path)
  try:
    yield
  finally:
    os.chdir(this_dir)

def test_remote(target_domain):
    while not web_paths.empty():
        path = web_paths.get()
        url =  f'{target_domain}{path}'
        time.sleep(2)
        r = requests.get(url)
        if r.status_code == 200:
            answers.put(url)
            sys.stdout.write(f'{GREEN}[+] {url} is up \n{RESET}')
        else :
            sys.stdout.write('[x]')
        sys.stdout.flush()

def run(target_domain):
    mythreads = list()
    for i in range(THREADS):
        print(f'Spawning thread {i}')
        t = threading.Thread(target=test_remote,args=(target_domain,))
        mythreads.append(t)
        t.start()
    for thread in mythreads:
        thread.join()

if __name__=='__main__':
    if len(sys.argv) == 3 : 
        with chdir('/home/thepunisher/Desktop/wordpress'):
            gather_paths()
        input('Press return to continue')
        target_domain = sys.argv[1]
        output = sys.argv[2]
        run(target_domain) 
        with open(output,'w') as f :
            while not answers.empty():
                f.write(f'{answers.get()} \n')
        print('Done, results save in {output}')
    else :
        print("Example : python mapper.py wordpress.com wordpress.txt")