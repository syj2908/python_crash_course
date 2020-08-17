file_path = "text_files\programming.txt"
while 1:
    name = input(r"May I know your name?(input 'q'to quit) ")
    if name == "q":
        break
    print("Hello "+name+"!\n")
    with open(file_path, 'a') as file_object:
        file_object.write(name+"\n")
