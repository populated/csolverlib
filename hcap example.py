import warnings
from CSolver.Hcap.hcap import Solver
import time
from colorama import Fore
import math
import threading
import ctypes
import os
import keyboard

warnings.filterwarnings("ignore", message="Curlm already closed! quitting from process_data")
warnings.filterwarnings("ignore", message="Curlm alread closed!", category=UserWarning)

success_count = 0
fail_count = 0
total_attempts = 0
total_time = 0
lock = threading.Lock()
stop_signal = False

def update_console_title():
    global success_count, fail_count, total_attempts
    avg_solve_rate = (success_count / total_attempts) * 100 if total_attempts > 0 else 0
    title = f"CSolver | {success_count}/{total_attempts} | {avg_solve_rate:.2f}%"
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)

def hCap():
    global success_count, fail_count, total_attempts, total_time
    while not stop_signal:
        start = time.time()
        cap = Solver(
            api_key="csolver api key"
            sitekey='f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34', # sitekey to match the url provided
            site='discord.com', # Site the captcha is on
            proxy="user:pass@ip:port" # Can be 'None' or ''
            rqdata="" # Can be 'None' or ''
        ).solve() # solve the captcha
        end = time.time()
        elapsed = end - start
        e = round(elapsed, 2)

        with lock:
            total_attempts += 1
            total_time += elapsed
            if cap: # was the solve successful?
                print(Fore.LIGHTCYAN_EX + f"Solved hCaptcha {Fore.YELLOW}[ {Fore.LIGHTBLUE_EX}{cap[:75]}***{Fore.YELLOW} ] {Fore.YELLOW}[{Fore.LIGHTBLUE_EX} {e}s{Fore.YELLOW} ]")
                with open("solved.txt", 'a') as f: # writes solution to a file [ debugging purposes ] 
                    f.write(f"{cap}\n")
                return cap # returns the captcha solution
            else:
                fail_count += 1
                print(Fore.LIGHTRED_EX + f"Failed to solve hCaptcha {Fore.YELLOW}[ {Fore.LIGHTBLUE_EX}{e}s {Fore.YELLOW}]")
            update_console_title()
            
threads = []
for i in range(1):
    thread = threading.Thread(target=hCap)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
