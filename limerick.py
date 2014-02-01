#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = []

from itertools import izip, product
from collections import defaultdict

from arxiv import get_article
from nlp import pronunciation, score_rhyme


def parse_article(aid):
    raw, tokens = get_article(aid)
    sentences = defaultdict(list)
    for sent, token_list in izip(raw, tokens):
        try:
            w, p, s, c = pronunciation(token_list)
        except KeyError:
            continue
        sentences[c].append((sent, w, p, s))
    return sentences


if __name__ == "__main__":
    aid = "1310.4179"
    # aid = "1309.0653"
    doc = parse_article(aid)

    short = []
    for k in range(5, 11):
        short += doc[k]

    lng = []
    for k in range(11, 18):
        lng += doc[k]

    for i, s1 in enumerate(lng):
        for s2 in lng[i+1:]:
            if s1[1][-1].lower() == s2[1][-1].lower():
                continue
            score = score_rhyme(s1[2], s2[2])
            if score > 0.5:
                print(score)
                print(s1[0])
                print(s2[0])
                print()
