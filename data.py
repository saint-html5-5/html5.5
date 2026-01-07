import os
import re
import sys
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# ANSI escape sequences for colored text
CLEAR_SCREEN = '\033[2J'
RED = '\033[31m'   # mode 31 = red foreground
BLUE = "\033[34m"
CYAN = "\033[36m"
GREEN = "\033[32m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the logo with colors
def logo():
    clear_screen()
    colors = [36, 32, 34, 35, 31, 37]

    logo_text = r"""
    ███╗   ███╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗███╗   ███╗ █████╗ ██╗  ██╗███████╗██████╗ ███████╗
    █████╗████║██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝████╗ ████║██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██╔════╝
    ██╔████╔██║██║   ██║██╔██╗ ██║█████╗   ╚████╔╝ ██╔████╔██║███████║█████╔╝ █████╗  ██████╔╝███████╗
    ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══╝    ╚██╔╝  ██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗╚════██║
    ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║███████╗   ██║   ██║ ╚═╝ ██║██║  ██║██║  ██╗███████╗██║  ██║███████║
    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
                    |\     /|\     /|\     /|\     /|\     /|\     /|\     /|
                    | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
                    | |   | | |   | | |   | | |   | | |   | | |   | | |   | |
                    | |N  | | |e  | | |t  | | |w  | | |o  | | |r  | | |k  | |
                    | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
                    |/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|
                                                         
                        Discord: https://whop.com/moneymakers-network/
    """

    for line in logo_text.split("\n"):
        sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, RESET))
        time.sleep(0.02)

# Global set and counter to track unique emails and duplicates
lock = threading.Lock()
seen_emails = set()
total_duplicates = 0

def extract_and_save_emails(file_path, output_file, duplicate_file):
    global total_duplicates

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)

    unique_emails = []
    duplicate_emails = []
    with lock:
        for email in email_matches:
            clean_email = email.split(':')[0]
            if clean_email in seen_emails:
                total_duplicates += 1
                duplicate_emails.append(clean_email)
            else:
                seen_emails.add(clean_email)
                unique_emails.append(clean_email)

    # Writing emails to the files after releasing the lock
    if unique_emails:
        with lock:
            output_file.write('\n'.join(unique_emails) + '\n')
    if duplicate_emails:
        with lock:
            duplicate_file.write('\n'.join(duplicate_emails) + '\n')

def process_folder(folder_path):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(('.pdf', '.csv', '.txt')):
                all_files.append(file_path)

    print(f"Total files to process: {len(all_files)}")

    with open('all.txt', 'a', encoding='utf-8') as output_file, open('duplicate.txt', 'a', encoding='utf-8') as duplicate_file:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(extract_and_save_emails, file_path, output_file, duplicate_file) for file_path in all_files]
            for future in futures:
                future.result()  # Ensure all threads complete

    print(f"Total duplicates removed: {total_duplicates}")

if __name__ == "__main__":
    logo()  # Display the logo first
    folder_path = '.'  # Specify your folder path here
    process_folder(folder_path)
