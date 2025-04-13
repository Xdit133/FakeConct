import os
import subprocess
import random
import time
from colorama import Fore, Style, init
def install_requirements():
    requirements = """
    colorama
    """
    with open("requirements.txt", "w") as req_file:
        req_file.write(requirements.strip())
    os.system("pip install -r requirements.txt")
def get_random_commit_message():
    with open("reason.txt", "r") as f:
        messages = f.readlines()
    return random.choice(messages).strip()
def print_banner():
    os.system("title made BY imscruz | do not try spamming!")
    print(Fore.WHITE + Style.BRIGHT + """
___________       __          _________                       
\_   _____/____  |  | __ ____ \_   ___ \  ____   ____   ____  
 |    __) \__  \ |  |/ // __ \/    \  \/ /  _ \ /    \_/ ___\ 
 |     \   / __ \|    <\  ___/\     \___(  <_> )   |  \  \___ 
 \___  /  (____  /__|_ \\___  >\______  /\____/|___|  /\___  >
     \/        \/     \/    \/        \/            \/     \/ 

    """ + Style.RESET_ALL)
    print(Fore.WHITE + "Made by imscruz!" + Style.RESET_ALL)
def fake_contributions():
    print_banner()
    repo_link = input(Fore.YELLOW + "Enter the repository link: " + Style.RESET_ALL)
    folder_name = input(Fore.YELLOW + "Enter the folder name to create: " + Style.RESET_ALL)
    contributions_count = int(input(Fore.YELLOW + "How many contributions do you want to make? " + Style.RESET_ALL))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(folder_name)
    subprocess.run(["git", "clone", repo_link, "."])
    for i in range(contributions_count):
        file_name = f"file_{random.randint(1, 10000)}.txt"
        with open(file_name, "w") as f:
            f.write(f"Fake content for commit {i + 1}")
        subprocess.run(["git", "add", file_name])
        commit_message = get_random_commit_message()
        subprocess.run(["git", "commit", "-m", commit_message])
        
        time.sleep(3)
    subprocess.run(["git", "push", "origin", "main"])
    print(Fore.GREEN + f"Successfully made {contributions_count} fake contributions!" + Style.RESET_ALL)
if __name__ == "__main__":
    install_requirements()
    fake_contributions()
