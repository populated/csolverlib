from threading import Thread
import time
from colorama import Fore
from csolver import Solver # import ReCap solver from CSolver 

solver = Solver() # initialize solver

def recap():
    while True:
        start = time.time()
        cap = solver.solve_recap( # Solve the captcha
            False, # Is the captcha invisible? 
            "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeMrv8ZAAAAAIcvo5HKvdj1lxtUdHnS13jUCulQ&co=aHR0cHM6Ly9wbGF5Lmhib21heC5jb206NDQz&hl=en&v=MuIyr8Ej74CrXhJDQy37RPBe&size=invisible&cb=f9q60qxahq1b", # The POST request to recaptcha [ also tell you if it is invisible or not ] 
            "https://www.google.com/recaptcha/enterprise/reload?k=6LeMrv8ZAAAAAIcvo5HKvdj1lxtUdHnS13jUCulQ" # The recaptcha GET request
        )
        end = time.time()
        elapsed = round(end - start, 2)

        if cap:
            print(Fore.LIGHTCYAN_EX + f"Solved ReCaptcha {Fore.YELLOW}[ {Fore.LIGHTBLUE_EX}{cap[:75]}***{Fore.YELLOW} ] {Fore.YELLOW}[{Fore.LIGHTBLUE_EX} {elapsed}s{Fore.YELLOW} ]")
            with open("solved.txt", 'a') as f: # saves solutions to a txt [ For debugging purposes ]
                f.write(f"{cap}\n")
            return cap # returns the captcha solution 
        else:
            print(Fore.LIGHTRED_EX + f"Failed to solve ReCaptcha {Fore.YELLOW}[ {Fore.LIGHTBLUE_EX}{elapsed}s {Fore.YELLOW}]")
            continue # retries in case of failure

def solve(t):
    threads = []
    for _ in range(t):
        thread = Thread(target=recap)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    threads = 10 # how many captchas to solve at once
    while True: # contonuously solve until closed
        solve(threads)
