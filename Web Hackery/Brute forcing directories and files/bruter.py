import queue
import requests
import threading
import sys
import shutil

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
EXTENSIONS = ['.php', '.bak', '.orig', '.inc','.js','.css']
#TARGET = "http://testphp.vulnweb.com"
THREADS = 50
GREEN = '\033[92m'  
RESET = '\033[0m'
RED = '\033[91m'

def print_banner():
    skull = r"""
     _____
    /     \
   | () () |
    \  ^  /
     |||||
     |||||
    """
    
    program_name = "Anguilla Buster"
    
    print(RED+skull+RESET)
    print(GREEN + program_name + RESET)
    print("\n" + "="*30 + "\n")

def get_words(wordlist):
    with open(wordlist, 'r') as file:
       raw_words = [line.strip() for line in file.readlines()]  # Supprimer les espaces vides

    words = queue.Queue()   

    for word in raw_words:
        words.put(f"/{word}/")  # Ajouter /[mot]/
    
    for ext in EXTENSIONS:
        words.put(f"/{word}{ext}")  # Ajouter /[mot][extension]
    return words

import requests
import sys

# Constantes (assure-toi de définir AGENT, GREEN, RED, RESET quelque part)
AGENT = "Your User-Agent"  # Définis ton User-Agent ici
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

file_lock = threading.Lock()

def dir_bruter(words, target, output):
    headers = {'User-Agent': AGENT}
    
    while not words.empty():
        url = f'{target}{words.get()}'
        try:
            r = requests.get(url, headers=headers)
        except requests.RequestException:  # Gérer les erreurs liées aux requêtes
            sys.stderr.write('x')
            sys.stderr.flush()
            continue

        if r.status_code == 200:
            print(f'\n {GREEN}Success ({r.status_code}:{url}){RESET}')
            
            # Utilisation du verrou juste pour l'écriture dans le fichier
            with file_lock:
                with open(output, 'a') as file:  # Mode 'a' pour ajouter au fichier sans écraser
                    file.write(f'{r.status_code}:{url} \n')
                    
        elif r.status_code == 404:
            print(f'\n {RED}Not found ({r.status_code}:{url}){RESET}')
        else:
            print(f'\n {r.status_code} => {url}')


if __name__=='__main__':
    print_banner()
    if len(sys.argv)<2 or len(sys.argv)>4:
        print("Exemple of use : python bruter.py site.com wordlist.txt output.txt")
    else :
        target=sys.argv[1]
        if len(sys.argv)==2:
            #set wordlist by default
            wordlist = 'all.txt'
            output = 'output.txt'
        elif len(sys.argv)==3:
            wordlist = sys.argv[2]
            output = 'output.txt' # set default output
        elif len(sys.argv)==4:
            output = sys.argv[3]
        words = get_words(wordlist)
        #!print('Press to continue')
        #sys.stdin.readline()
        with open(output, 'w') as file:
            pass  # clean output file before start
        file.close()
        for _ in range(THREADS):
            t = threading.Thread(target=dir_bruter,args=(words,target,output))
            t.start()
