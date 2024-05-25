# ameliore watson4 en ajoutant a 'while True' pour faire une boucle infinie
# bien penser à ajouter une condition de sortie avec des exit_words

def init_watson(config_filename):
    """
    load the config_file_name and returns set of
    sentiment words in a tuple

    parameter
    ---------
    config_file_name: the name of the file to load

    return
    ------
    the tuple of sets (positive_words, negative_words, exit_words)
    """
    positive_words, negative_words, exit_words = set(), set(), set()
    with open(config_filename, "r", encoding="utf8") as f:
        for line in f:
            # we remove the \n char is if it is at the end of the line
            # it might not be the case at the end of the file
            line = line.rstrip()
            if not line:
                continue
            kind, *words = line.split()
            match kind:
                case "POSITIVE":
                    positive_words.update(set(words))
                case "NEGATIVE":
                    negative_words.update(set(words))
                case "EXIT":
                    exit_words.update(set(words))

    return positive_words, negative_words, exit_words


def test_phrase_sentiment(sentence, sentiment):
    """
    take a sentence and return True if any words
    in sentiment is in phrase

    parameter
    ---------
    phrase: a set of str
    sentiment: a set of str containing sentiment words

    return
    ------
    the interection between the words in the sentence and the words
    in the sentiment set
    """
    return sentence.intersection(sentiment)


def watson():
    """
    start doctor watson
    """
    positive_words, negative_words, exit_words = init_watson(
        "watson-config.txt"
    )

    prompt = 'bonjour, à vous: '
    while True:
        phrase = set(input(prompt).lower().split())

        if test_phrase_sentiment(phrase, negative_words):
            prompt = "Ohhhh, c'est triste, mais encore...\n"
        elif test_phrase_sentiment(phrase, positive_words):
            prompt = "C'est super, mais encore...\n"
        elif test_phrase_sentiment(phrase, exit_words):
            break
        elif not phrase:
            prompt = "Tu n'es pas bavard. Que peux-tu me dire...\n"
        else:
            prompt = "je ne comprends pas...\n"

    print("C'est fini, au revoir !")


if __name__ == "__main__":
    watson()
