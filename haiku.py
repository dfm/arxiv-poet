from nltk.corpus import cmudict
import nltk
import string
import numpy as np
import arxiv

sentence = "We introduce a stable, well tested Python implementation of the affine-invariant ensemble sampler for Markov chain Monte Carlo (MCMC) proposed by Goodman & Weare (2010). The code is open source and has already been used in several published projects in the astrophysics literature."

# st = arxiv.get_article("1202.3665")
st = arxiv.get_article("1401.6128")
# st = nltk.sent_tokenize(sentence)
ph = cmudict.dict()
sent_syls = np.empty(len(st))

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

nsyls = []
for sentence in st:
    word_list = syl_count(sentence)
    if word_list != None:
#         nsyls.append(sum([w[1] for w in word_list]))
        if sum([w[1] for w in word_list]) == 17:
            n = 0
            m = 0
            for word in word_list:
                n += word[1]
                if n == 5:
                    for word in word_list:
                        m += word[1]
                        if m == 12:
                            print sentence

# print nsyls
# a = np.where(np.array(nsyls) == 17)[0]
# haiku = st[a]
# print haiku
raw_input('enter')

# Count number of syllables in each sentence
for i, wt in enumerate(st):
#     wt = nltk.word_tokenize(s)
    tot_syls = 0
    for full_word in wt:
        if not len(full_word.strip(string.punctuation)): continue
        words = full_word.split("-")
        for w in words:
            try:
                phs =  ph[w.lower()][0]
                for p in phs:
                    tot_syls += (p.count('0') + p.count('1') + p.count('2'))
            except KeyError:
                tot_syls = 0
                break
#                 print "Failed on: ", w
    sent_syls[i] = tot_syls

print sent_syls
a = np.where(sent_syls == 17)[0]
haiku = st[a[1]]

print haiku
