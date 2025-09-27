import yaml

def write_sample(output):
    root = {
        'a': [0, 1, 2],
        'b': (3, 4, 5),
        # can serialize sets in YAML
        # (although this might not survive
        # if read by other languages though)
        12: {6, 7, 8},
        # can also serialize a tuple as a key
        # (same warning applies)
        (2, 5): {0: True, 1: False},
    }
    with open(output, 'w') as writer:
        yaml.dump(root, writer)

def read_sample(filename):
    with open(filename, 'r') as feed:
        return yaml.load(feed, yaml.FullLoader)

SAMPLE = "data/tiny.yaml"

def main():
    write_sample(SAMPLE)
    loop = read_sample(SAMPLE)
    print(f"after save in {SAMPLE} -> read we find\n{loop=}")

main()