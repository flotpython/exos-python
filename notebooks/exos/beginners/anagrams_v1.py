"""
pareil mais continue jusqu'à ce qu'on entre 'exit'
"""

def are_anagrams(word1, word2):
    return sorted(word1.lower()) == sorted(word2.lower())

def main():
    while True:
        mot1 = input("entrez le mot #1 ")
        if mot1 == 'exit':
            break
        mot2 = input("entrez le mot #2 ")
        if mot2 == 'exit':
            break
        print ("oui" if are_anagrams(mot1, mot2) else "non")
    print("bye")

if __name__ == '__main__':
    main()
