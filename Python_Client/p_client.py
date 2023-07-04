import os
import requests
from colorama import Fore

BASE_URL = "http://localhost:5000"

def print_title():
    print(Fore.YELLOW + "PPTX Analyzer" + Fore.RESET)

def print_menu():
    print("\n" + Fore.YELLOW + "-- Main Menu --")
    print("-" * 24)
    print("| [1] Upload new pptx |")
    print("| [2] Check status    |")
    print("| [3] Get results     |")
    print("| [4] Exit            |")
    print("-" * 24 + Fore.RESET)

def print_status(id, status):
    print("\n-- Status of ID {} --".format(id))
    print("Status: " + (Fore.GREEN if status == 'complete' else Fore.RED) + status + Fore.RESET)

def print_result(id, analysis):
    print("\n-- Results of ID {} --\n".format(id))
    print(analysis['result'])

def upload():
    path = input("Enter the full path to the pptx file: ")
    if not os.path.exists(path):
        print("The specified file does not exist.")
        return
    with open(path, 'rb') as f:
        files = {'file': f}
        r = requests.post(f'{BASE_URL}/upload', files=files)
        print(r.json()['message'] if r.status_code == 201 else 'Error in file upload')

def check_status():
    id = input("Enter the analysis ID: ")
    r = requests.get(f'{BASE_URL}/status/{id}')
    print_status(id, r.json()['status']) if r.status_code == 200 else print('Error in status check')

def get_results():
    id = input("Enter the analysis ID: ")
    r = requests.get(f'{BASE_URL}/result/{id}')
    print_result(id, r.json()) if r.status_code == 200 else print('Error in fetching results')

def main():
    print_title()
    while True:
        print_menu()
        choice = int(input())
        if choice == 1:
            upload()
        elif choice == 2:
            check_status()
        elif choice == 3:
            get_results()
        elif choice == 4:
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
