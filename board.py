from copy import deepcopy
from trie import Trie

class Coords:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Word:
    def __init__(self):
        self.word = ""
        self.combination = []

    def append(self, char: str, coords: Coords):
        self.word += char
        self.combination.append(coords)

    def pop_back(self):
        self.word = self.word[:-1]
        self.combination = self.combination[:-1]

    def length(self):
        return len(self.word)

    def get_word(self) -> str:
        return self.word

    def get_combination(self) -> list[Coords]:
        return self.combination




class Board:
    def __init__(self, trie: Trie, letters):
        self.trie: Trie = trie
        self.letters: list[list[str]] = letters
        self.words: list[Word] = []

        self._current_word: Word = Word()

        used_letters = [[False for x in range(4)] for y in range(4)]

        self.used_letters: list[list[bool]] = used_letters


    def _gen_words(self, x, y):
        # Break conditions
        if x not in range(4) or y not in range(4):
            return  # Not a valid place on board.
        if self.used_letters[x][y]:
            return  # Letter already used.
        if self._current_word.length() + 1 > 13:
            return  # Word will be longer than max length.
        if not self.trie.is_predecessor(self._current_word.get_word() + self.letters[x][y]):
            return  # There are no word starting this way.

        self._current_word.append(self.letters[x][y], Coords(x, y))
        self.used_letters[x][y] = True

        if self.trie.is_word(self._current_word.get_word()) and self._current_word.length() >= 3:
            self.words.append(deepcopy(self._current_word))

        for y_dir in [-1, 0, 1]:
            for x_dir in [-1, 0, 1]:
                x_new = x + x_dir
                y_new = y + y_dir
                self._gen_words(x_new, y_new)

        self._current_word.pop_back()
        self.used_letters[x][y] = False

    def generate_words(self):
        for y in range(4):
            for x in range(4):
                self._gen_words(x, y)
        self.words.sort(key= lambda x: x.get_word())
        self.words.sort(key= lambda x: x.length(), reverse=True)

    def get_words(self) -> list[Word]:
        return self.words
