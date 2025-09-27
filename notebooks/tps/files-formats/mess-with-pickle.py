import pickle

def write_sample(output):
    root = {
        'a': [0, 1, 2],
        'b': (3, 4, 5),
        12: {6, 7, 8},
        (2, 5): {0: True, 1: False},
    }
    # we could have used pickle.dump()
    # but we want to see open(..., 'wb')
    with open(output, 'wb') as writer:
        writer.write(pickle.dumps(root))

def read_sample(filename):
    with open(filename, 'rb') as feed:
        return pickle.loads(feed.read())

SAMPLE = "data/tiny.pickle"

def main():
    write_sample(SAMPLE)
    loop = read_sample(SAMPLE)
    print(f"after save in {SAMPLE} -> read we find\n{loop=}")

main()