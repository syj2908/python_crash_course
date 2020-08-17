file_path="text_files\pi_million_digits.txt"
with open(file_path) as file_object:
    lines = file_object.readlines()
pi_string=""
for line in lines:
    pi_string += line.strip()
birthday = "000829"
if birthday in pi_string:
    print("succeed")
else:
    print("failed")