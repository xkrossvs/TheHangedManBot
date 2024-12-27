def get_word_list(file_name: str) -> list[str]:
    with open(f'data/{file_name}.txt', 'r', encoding="utf8") as file:
        words = file.readlines()
        words = [s.strip("\n") for s in words]
        return words
