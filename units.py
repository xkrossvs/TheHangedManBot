def find_all_indices(word, char):
    return [i for i, letter in enumerate(word) if letter == char]


def is_it_a_win(word, text_word):
    return ''.join(text_word) == word
