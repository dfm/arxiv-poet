#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["pronunciation", "score_rhyme"]

import string
from itertools import product, izip

from nltk.corpus import cmudict

pd = cmudict.dict()


def count_syllables(phonemes):
    count = 0
    for phoneme in phonemes:
        count += phoneme[-1] in string.digits
    return count


def pronunciation(tokens):
    phonemes = []
    for w in tokens:
        for sw in w.split("-"):
            p = pd[sw.lower()]
            phonemes.append((sw, p, count_syllables(p[0])))
    words, phonemes, syllables = zip(*phonemes)
    return words, phonemes, syllables, sum(syllables)


def distance(w1, w2):
    n = min(len(w1), len(w2))
    return sum([c1 == c2 for c1, c2 in izip(w1[:n], w2[:n])]) / n


def score_rhyme(p1, p2):
    # Flatten the phoneme lists.
    s1 = [[w for s in p for w in s] for p in product(*p1)]
    s2 = [[w for s in p for w in s] for p in product(*p2)]

    # Compute the suffix phoneme scores.
    score, norm = 0.0, 0.0
    for depth, v in izip(range(2, 6), [0.05, 0.15, 0.4, 0.4]):
        for s01, s02 in product(s1, s2):
            w1, w2 = "".join(s01[-depth:]), "".join(s02[-depth:])
            score += v * distance(w1, w2)
            norm += v
    score /= norm

    # Extract the vowels.
    v1 = [[w[:-1] for w in s if w[-1] in string.digits] for s in s1]
    v2 = [[w[:-1] for w in s if w[-1] in string.digits] for s in s2]
    dists = [distance(se1[-1], se2[-1]) for se1, se2 in product(v1, v2)]
    weights = [1/(i1+1)/(i2+1)
               for i1, i2 in product(range(len(v1)), range(len(v1)))]
    vscore = sum([d * w for d, w in izip(dists, weights)]) / sum(weights)

    a = 0.5
    return (1-a)*score + a*vscore


if __name__ == "__main__":
    w, p1, s, c = pronunciation(["Dude", "in", "an", "underwater", "tin"])
    w, p2, s, c = pronunciation(["Dude", "in", "an", "underwater", "tin"])
    print(score_rhyme(p1, p2))
