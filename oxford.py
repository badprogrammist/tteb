import io
import re
import string


class Oxford(object):
    def __init__(self, words):
        self._words = words

    def words(self):
        return self._words


def oxford_3000(filename="oxford-3000-words.txt"):
    def prepare(word):
        return word.strip()

    words = []

    with io.open(filename) as oxf:
        words = [prepare(line) for line in oxf.readlines()]

    return Oxford(words)


def oxford_stats(searcher):
    split_ex = re.compile(r"|".join(string.whitespace))

    def tokenize(text):
        return [token.lower()
                for token in split_ex.split(text)]

    oxf = oxford_3000()

    for word in oxf.words():
        print("{}: {}".format(word,
                              len(searcher.search(tokenize(word)))))