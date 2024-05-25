from unittest import TestCase

from motus import *

french = Dictionary("data/ods6.txt")

class Tests(TestCase):

    def test_matches1(self):

        h = Hidden("ABC")

        self.assertEqual(h.attempt("ABC").answer, Answer(R, R, R))
        self.assertEqual(h.attempt("BCA").answer, Answer(Y, Y, Y))
        self.assertEqual(h.attempt("ACB").answer, Answer(R, Y, Y))
        self.assertEqual(h.attempt("ABA").answer, Answer(R, R, B))

    def test_matches2(self):

        h = Hidden("ABCABC")

        self.assertEqual(h.attempt("ABCABC").answer, Answer(R, R, R, R, R, R))
        self.assertEqual(h.attempt("ABCXYZ").answer, Answer(R, R, R, B, B, B))
        self.assertEqual(h.attempt("ABCBCA").answer, Answer(R, R, R, Y, Y, Y))
        self.assertEqual(h.attempt("BCA---").answer, Answer(Y, Y, Y, B, B, B))
        self.assertEqual(h.attempt("ACB---").answer, Answer(R, Y, Y, B, B, B))
        self.assertEqual(h.attempt("A-B-A-").answer, Answer(R, B, Y, B, Y, B))


    # run massively on all words of a certain length
    def map_dict(self, hidden_str: str, on_dict: set[str], *, expect_exactly_one):

        hidden = Hidden(hidden_str)

        answers = [
            hidden.attempt(word).answer
            for word in on_dict
            if len(word) == len(hidden)
        ]
        if expect_exactly_one:
            all_red = [a for a in answers if a.right()]
            self.assertEqual(len(all_red), 1)

    def check_length(self, length):
        # pick one word of that length
        # and then run it against all words of that length
        self.map_dict(french.sample_of_length(length), french, expect_exactly_one=True)

    def test_dict_1(self):
        # for words that are 3/4/5/6 long
        for length in range(3, 7):
            self.check_length(length)

    def test_dict_2(self):
        # for words that are longer
        for length in range(7, 12):
            self.check_length(length)

    def solver(self, hidden_str, words):
        hidden = Hidden(hidden_str)
        attempts = [
            hidden.attempt(word) for word in words
        ]
        self.assertIn(
            hidden_str,
            french.compatible_words(attempts)
        )

    def test_solver(self):
        hidden = "francais"
        words = [ "filtrons", "fournils", "froufrou"]
        self.solver(hidden, words)
