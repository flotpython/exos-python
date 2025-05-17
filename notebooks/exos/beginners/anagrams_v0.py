"""
un programme qui demande deux mots
et qui vérifie si ce sont des anagrammes
"""

def are_anagrams(word1, word2):
    return sorted(word1.lower()) == sorted(word2.lower())

def main():
    mot1 = input("entrez le mot #1 ")
    mot2 = input("entrez le mot #2 ")
    if are_anagrams(mot1, mot2):
        print("oui")
    else:
        print("non")

if __name__ == '__main__':
    main()
