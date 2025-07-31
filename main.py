import os
import subprocess
import random
import time
import sys
import datetime
from getpass import getpass

try:
    from colorama import Fore, Style, init
except ImportError:
    print("Menginstall requirements...")
    os.system(f"{sys.executable} -m pip install colorama")
    from colorama import Fore, Style, init

init(autoreset=True)

# ========== SETTING ==========
repo_url = "-" // Your repo
folder_name = "-" // Folder name (free)
commits_per_batch = 50 // Number of commits per batch
year_start = 2021
year_end = 2025
git_email = "-" // Your email

commit_delay_min = 15
commit_delay_max = 45
batch_pause_min = 3600
batch_pause_max = 7200
auto_stop_batch = 3 // Number of batches, then stop
# ==========================================

def create_reason_file():
    if not os.path.exists("reason.txt"):
        with open("reason.txt", "w") as f:
            f.write(
"""Update content
Improve documentation
Fix typo
Refactor code
Add feature
Minor changes
Code clean up
Update README
Optimize code
Bug fix
""")
        print(Fore.YELLOW + "[INFO] File reason.txt not found, default created.")

def get_random_commit_message():
    with open("reason.txt", "r") as f:
        lines = [l.strip() for l in f if l.strip()]
    return random.choice(lines) if lines else "Update content"

def print_banner():
    if os.name == "nt":
        os.system("Created by imscruz | now recording version Xdit133 | Don't try to spam!")
    print(Fore.WHITE + Style.BRIGHT + """
___________       __          _________                       
\_   _____/____  |  | __ ____ \_   ___ \  ____   ____   ____  
 |    __) \__  \ |  |/ // __ \/    \  \/ /  _ \ /    \_/ ___\ 
 |     \   / __ \|    <\  ___/\     \___(  <_> )   |  \  \___ 
 \___  /  (____  /__|_ \\___  >\______  /\____/|___|  /\___  >
     \/        \/     \/    \/        \/            \/     \/ 
""" + Style.RESET_ALL)
    print(Fore.WHITE + Style.RESET_ALL)

def random_date(start_year, end_year):
    start_dt = datetime.datetime(start_year, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(end_year, 12, 31, 23, 59, 59)
    delta = end_dt - start_dt
    random_second = random.randint(0, int(delta.total_seconds()))
    result_dt = start_dt + datetime.timedelta(seconds=random_second)
    return result_dt.strftime("%Y-%m-%d %H:%M:%S")

def setup_repo(git_username, repo_link):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(Fore.CYAN + "[*] Cloning repository..." + Style.RESET_ALL)
        result = subprocess.run(["git", "clone", repo_link, folder_name])
        if result.returncode != 0:
            print(Fore.RED + "Failed to clone repo. Check your repo link!" + Style.RESET_ALL)
            sys.exit(1)
    os.chdir(folder_name)
    subprocess.run(["git", "config", "user.name", git_username])
    subprocess.run(["git", "config", "user.email", git_email])
    create_reason_file()
    subprocess.run(["git", "pull", "origin", "main"])

def fake_contributions_loop(git_username, repo_link):
    print_banner()
    setup_repo(git_username, repo_link)
    batch_count = 1
    while True:
        if auto_stop_batch and batch_count > auto_stop_batch:
            print(Fore.GREEN + f"\nAUTO-STOP: Has reached {auto_stop_batch} batches. Script stopped for safety reasons." + Style.RESET_ALL)
            break

        print(Fore.CYAN + f"\n=== Batch commit ke-{batch_count} ({commits_per_batch} commit) ===\n" + Style.RESET_ALL)
        for i in range(commits_per_batch):
            file_name = f"file_{random.randint(1, 10000)}_{int(time.time())}.txt"
            with open(file_name, "w") as f:
                f.write(f"Fake content for commit {batch_count}.{i + 1}")
            subprocess.run(["git", "add", file_name])
            commit_message = get_random_commit_message()
            commit_date = random_date(year_start, year_end)
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = commit_date
            env["GIT_COMMITTER_DATE"] = commit_date
            subprocess.run(["git", "commit", "-m", commit_message], env=env)
            print(Fore.YELLOW + f"[Batch {batch_count} | {i+1}/{commits_per_batch}] Commit: {commit_message} | {commit_date}" + Style.RESET_ALL)
            delay = random.uniform(commit_delay_min, commit_delay_max)
            print(Fore.LIGHTBLACK_EX + f"Delay {delay:.1f}s" + Style.RESET_ALL)
            time.sleep(delay)
        subprocess.run(["git", "branch", "-M", "main"])
        print(Fore.CYAN + f"[*] Moving batch {batch_count} to the main branch..." + Style.RESET_ALL)
        subprocess.run(["git", "push", "origin", "main"])
        print(Fore.GREEN + f"Batch {batch_count}: {commits_per_batch} Commit successfully pushed!\n" + Style.RESET_ALL)
        batch_count += 1
        pause = random.uniform(batch_pause_min, batch_pause_max)
        print(Fore.LIGHTBLUE_EX + f"Sleep for {pause/60:.2f} minutes before the next batch..." + Style.RESET_ALL)
        time.sleep(pause)
        subprocess.run(["git", "pull", "origin", "main"])

if __name__ == "__main__":
    print("Enter your GitHub username:")
    git_username = input("Username: ")
    print("Enter Personal Access Token (not visible):")
    git_token = getpass("Token: ")
    repo_link = f"https://{git_username}:{git_token}@{repo_url}"
    try:
        fake_contributions_loop(git_username, repo_link)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[STOP] Stopped by user. All recent commits have been pushed." + Style.RESET_ALL)
