import json
file_path = r"text_files\username.json"
try:
    with open(file_path) as f_obj:
        username = json.load(f_obj)
except FileNotFoundError:
    username = input("What's your name? ")
    with open(file_path, 'w') as f_obj:
        json.dump(username, f_obj)
        print("We will remember you when you come back, " + username + "!")
else:
    print("Hello, "+username+"!")