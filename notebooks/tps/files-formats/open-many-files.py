def open_files(filename, n):
    files = []
    for i in range(1, n+1):
        try:
            files.append(open(filename))
        except:
            print(f"failed to open {i}-th file")
            break
    return files

from  argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("nbfiles", type=int)
    args = parser.parse_args()

    n = args.nbfiles
    print(f"we have received {n=}")

    # let's create a dummy file

    martyr_filename = "tmp.txt"

    with open(martyr_filename, 'w') as writer:
        print("hello world", file=writer)

    open_files(martyr_filename, n)

    print("DONE")

main()