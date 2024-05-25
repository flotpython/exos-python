import json

def write_sample(output):
    root = {
        'a': [0, 1, 2],
        'b': (3, 4, 5),
        # cannot serialize sets in JSON
        12: [6, 7, 8],
        # cannot serialize a tuple as a key
        '2x5': {0: True, 1: False},
    }
    with open(output, 'w') as writer:
        writer.write(json.dumps(root))

def read_sample(filename):
    with open(filename, 'r') as feed:
        return json.loads(feed.read())

SAMPLE = "tiny.json"

def main():
    write_sample(SAMPLE)
    loop = read_sample(SAMPLE)
    print(f"after save in {SAMPLE} -> read we find\n{loop=}")

main()