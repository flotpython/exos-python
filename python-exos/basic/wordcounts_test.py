from wordcounts import WordCounts

wc = WordCounts("wordcounts-data.txt")

print(wc)

# a Counter is a dictionary

print("----")
for word in ['arthur', 'people']:
    print(f"`{word}` was found {wc.counter[word]} times")

print("----")
matches = [ (w, c) for (w, c) in wc.counter.items() if 30 <= c <= 40]
for (w, c) in sorted(matches, key=lambda t: t[1]):
    print(f"`{w}` appears {c} times (b/w 30 and 40)")