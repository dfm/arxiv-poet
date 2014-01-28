from nltk.corpus import cmudict
import nltk
import string
import numpy as np
import arxiv

ph = cmudict.dict()

# Count the number of syllables in each word, for each sentence
# if a word isn't recognised, throw sentence away
def syl_count(st):
    word = []
    syls = []
    for full_word in st:
        word_syls = 0
        if not len(full_word.strip(string.punctuation)): continue
        words = full_word.split("-")
        for w in words:
            try:
                phs = ph[w.lower()][0]
                for p in phs:
                    word_syls += (p.count('0') + p.count('1') + p.count('2'))
                word.append(w)
                syls.append(word_syls)
            except KeyError:
                return None
    return zip(word, syls)

# Find Haikus from list of tuples of words and syllables
def find_haiku(st):
    nsyls = []
    for sentence in st:
        word_list = syl_count(sentence)
        if word_list != None:
            if sum([w[1] for w in word_list]) == 17:
                n = 0
                m = 0
                for word in word_list:
                    n += word[1]
                    if n == 5:
                        for word in word_list:
                            m += word[1]
                            if m == 12:
                                return sentence
    return 'No Haiku found'

# Find sentences with 5, 7 or 12 syllables
def find_alt_forms(st):
    nsyls = []
    for sentence in st:
        word_list = syl_count(sentence)
        if word_list != None:
            sylno = sum([w[1] for w in word_list])
            if sylno == 5: print sylno
            elif sylno == 7: print sylno
            elif sylno == 12: print sylno


def load_paper(arxiv_id):
    return arxiv.get_article(arxiv_id)

# 1202.3665 emcee paper
# 1306.3701 Van saders
# 1307.3239 Tom's paper
# 1401.6128 Fengji's paper
sk1 = "1309.0419"

st = load_paper(sk1)
print find_haiku(st)
print find_alt_forms(st)
