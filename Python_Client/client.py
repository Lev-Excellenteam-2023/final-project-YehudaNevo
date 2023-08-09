import os

import requests

API_URL = 'http://localhost:5000'


def print_options():
    print("\nChoose an option:")
    print("1. Get list of users")
    print("2. Get uploads for a user")
    print("3. Create a new user")
    print("4. Upload a file")
    print("5. Quit")


def get_users():
    response = requests.get(f'{API_URL}/users')
    print(response.json())


def get_user_uploads():
    user_id = int(input("Enter user ID: "))
    response = requests.get(f'{API_URL}/user/{user_id}/uploads')
    print(response.json())


def create_user():
    email = input("Enter user email: ")
    response = requests.post(f'{API_URL}/create_user', json={'email': email})
    print(response.json())


def upload_file():
    user_id = int(input("Enter user ID: "))
    filename = input("Enter filename: ")
    url = f'{API_URL}/upload_file'

    with open(filename, 'rb') as file:
        data = {'id': user_id}
        files = {'file': file}
        response = requests.post(url, data=data, files=files)

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")


def main():
    while True:
        print_options()
        choice = input("Enter your choice: ")
        if choice == '1':
            get_users()
        elif choice == '2':
            get_user_uploads()
        elif choice == '3':
            create_user()
        elif choice == '4':
            upload_file()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
