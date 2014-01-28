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


def compute(args):
    s1, s2 = args
    for i, (c1, c2) in enumerate(izip(s1[::-1], s2[::-1])):
        if c1 != c2:
            break
    return min(4.0, i) / 4.0


def score_rhyme(p1, p2, a=0.6):
    # Flatten the phoneme lists.
    s1 = [[w for s in p for w in s] for p in product(*p1)]
    s2 = [[w for s in p for w in s] for p in product(*p2)]

    # Reject the sentence if any pronunciations are identical.
    if any([t1 == t2 for t1, t2 in product(s1, s2)]):
        return 0

    # Compute the score for each combination.
    scores = map(compute, product(s1, s2))
    score = sum(scores) / len(scores)

    # Extract the vowels.
    v1 = [[w[:-1] for w in s if w[-1] in string.digits] for s in s1]
    v2 = [[w[:-1] for w in s if w[-1] in string.digits] for s in s2]
    dists = [distance(se1[-1], se2[-1]) for se1, se2 in product(v1, v2)]
    weights = [1/(i1+1)/(i2+1)
               for i1, i2 in product(range(len(v1)), range(len(v1)))]
    vscore = sum([d * w for d, w in izip(dists, weights)]) / sum(weights)

    return (1-a)*score + a*vscore


if __name__ == "__main__":
    w, p1, s, c = pronunciation(["Dude", "in", "an", "underwater", "tin"])
    w, p2, s, c = pronunciation(["Dude", "in", "an", "underwater", "spin"])
    print(score_rhyme(p1, p2))
