from nltk.corpus import cmudict
import nltk
import string
import numpy as np

sentence = "We introduce a stable, well tested Python implementation of the affine-invariant ensemble sampler for Markov chain Monte Carlo (MCMC) proposed by Goodman & Weare (2010). The code is open source and has already been used in several published projects in the astrophysics literature."

st = nltk.sent_tokenize(sentence)
ph = cmudict.dict()
sent_syls = np.empty(len(st))

for i, s in enumerate(st):
    wt = nltk.word_tokenize(s)
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
                pass
#                 print "Failed on: ", w
    sent_syls[i] = tot_syls

print sent_syls
