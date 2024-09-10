with open('win_stickers.txt', 'r', encoding="utf8") as file:
    win_stickers = file.readlines()
    win_stickers = [s.strip("\n") for s in win_stickers]