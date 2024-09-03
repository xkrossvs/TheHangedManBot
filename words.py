with open('words.txt', 'r', encoding="utf8") as file:
    words = file.readlines()
    words = [s.strip("\n") for s in words]
