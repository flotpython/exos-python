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
    while True:
        typed = input("Your guess ? ")
        try:
            attempt = hidden.attempt(typed)
            print(attempt)
            if attempt.answer.right():
                print("You won !")
                break
        except ValueError as e:
            print(e)

main()
