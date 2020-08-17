import json
file_path = r"text_files\favorite_number.json"
try:
    with open(file_path) as f_obj:
        number = json.load(f_obj)
except:
    number = input(r"Input your favorite number: ")
    with open(file_path, 'w') as f_obj:
        json.dump(number, f_obj)
else:
    print("I know your favorite number is "+number+"!")