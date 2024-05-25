from motus import Dictionary, Hidden

from argparse import ArgumentParser

def main():
    dictionary = Dictionary("ods6.txt")

    parser = ArgumentParser()
    parser.add_argument("--length", type=int, default=0)
    parser.add_argument("secret", nargs="?", default=None)
    args = parser.parse_args()

    if args.secret:
        n_letters = len(args.secret)
        secret = args.secret
    else:
        n_letters = args.length or int(input("How many letters ? "))
        secret = dictionary.sample_of_length(n_letters)
    hidden = Hidden(secret)
    attempts = []
    while True:
        typed = input("Your guess ? ")
        if typed.startswith("?"):
            command = typed[1:]
            match command:
                case "help":
                    print("?help: this help")
                    print("?howmany: how many words in the dictionary would match")
                    print("?words: displays the words in the dictionary would match")
                    print("?quit: quit the game")
                case "howmany" | "words":
                    possibles = dictionary.compatible_words(attempts, len(secret))
                    match command:
                        case "howmany":
                            print(f"{len(possibles)} words would match")
                        case "words":
                            for possible in possibles:
                                print(possible)
                case "quit":
                    print("Bye !")
                    return
            continue

        try:
            attempt = hidden.attempt(typed)
            print(attempt)
            attempts.append(attempt)
            if attempt.answer.right():
                print("You won !")
                break
        except ValueError as e:
            print(e)

main()
