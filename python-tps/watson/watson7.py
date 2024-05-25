# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

# v7: refactored

# for smart argument parsing and integrated help
import argparse

# for type hints
Name = str


# not everything is needed, but just to illustrate dunder methods...
class Sentence:

    def __init__(self, sentence):
        self.sentence = sentence
        self.words = self.sentence.split()

    def __str__(self):
        return str(self.sentence)

    def __contains__(self, word):
        return word in self.sentence

    def __len__(self):
        return len(self.words)

    def __getitem__(self, i):
        return self.words[i]


class Feeling:

    def __init__(self, name, words):
        self.name = name
        self.words = set(words)

    def resonates(self, sentence : Sentence) -> bool:
        """
        returns whether the sentence contains any word in the feeling
        """
        return self.words & {word.lower() for word in sentence.words}

    def outline(self, sentence : str) -> str:
        """
        returns sentence, but with the words in the feeling outlined
        """
        def outline(word):
            return f"*{word}*" if word.lower() in self.words else word
        return " ".join(outline(word) for word in sentence.words)


class Watson:

    # could go in the config as well, but would probably require
    # an alternative format like e.g. yaml
    answers = {
        'POSITIVE': "C'est super, mais encore...",
        'NEGATIVE': "Ohhhh, c'est triste, mais encore...",
        'EXIT': "C'est fini, au revoir !"
    }


    def __init__(self, config_filename):
        self.config_filename = config_filename
        # store in self.feelings a dict NAME -> Feeling
        self.feelings = dict()
        with open(config_filename, "r", encoding="utf8") as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    continue
                name, *words = line.split()
                self.feelings[name] = Feeling(name, words)

    def run(self, debug=False):
        prompt = 'bonjour, à vous: '
        active = True
        while active:
            sentence = Sentence(input(prompt).lower())
            for name, feeling in self.feelings.items():
                if feeling.resonates(sentence):
                    print(self.answers[feeling.name])
                    if debug:
                        print("DEBUG:", feeling.outline(sentence))
                    if name == 'EXIT':
                        active = False
                    break
            else:
                print("je ne comprends pas...")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config", default="watson-config.txt",
        help="give the config file to load feelings")
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="print debug information")

    args = parser.parse_args()
    Watson(args.config).run(args.debug)
