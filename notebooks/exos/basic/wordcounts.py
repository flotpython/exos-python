"""
playing with word frequencies
"""

from collections import Counter
from string import punctuation

# the text has unicode quotes in it
punctuation +=  "“”"

class WordCounts:

    def __init__(self, filename) -> None:
        # just in case, keep for future reference
        self.filename = filename

        # the words as they appear in the text, all lowercase and with punctuation removed
        words = []

        # read and erase punctuation
        with open(self.filename) as feed:
            for line in feed:
                line = line.strip().lower()
                for char in punctuation:
                    line = line.replace(char, " ")
                # add the words in the list
                words.extend(line.split())

        # using Counter makes it easier
        self.counter = Counter(words)

    def __repr__(self) -> str:
        result = ""
        result += f"{self.filename}:"
        result += f" {self.size()} total words"
        result += f"{len(self.vocabulary())} different words"
        result += "\n".join(f"  {w:>5} : {c}" for w, c in self.counter.most_common(5))
        return result

    def size(self) -> int:
        """
        number of words in the original text
        """
        # only in 3.10
        #return self.counter.total()
        # a Counter is a dict
        return sum(value for value in self.counter.values())

    def vocabulary(self) -> set[str]:
        """
        return the set of words used in the text
        """
        return set(self.counter.elements())

    # pour la variante
    def __getitem__(self, word: str) -> int:
        return self.counter[word]
