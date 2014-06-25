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
    s51 = []; s7 = []; s52 = []
    for sentence in st:
        word_list = syl_count(sentence)
        if word_list != None:
            if sum([w[1] for w in word_list]) == 17:
                n = 0; m = 0; l = 0
                for word in word_list:
                    n += word[1]
                    m += word[1]
                    l += word[1]
#                     s51.append(word[0])
                    if n == 5:
                        for word in word_list:
#                             s7.append(word_list[m][0])
#                             s7 = word_list[0,5:12]
                            m += word[1]
                            l += word[1]
                            if m == 12:
                                for word in word_list:
#                                     s52.append(word_list[l][0])
#                                     s52 = word_list[0,12:]
                                    l += word[1]
                                    if l == 17:
#                                         print l
                                        return build_sentence(sentence)
#                                         return build_sentence(s51) + "\n", \
#                                                 build_sentence(s7) + "\n", \
#                                                 build_sentence(s52)
    return " "

# Find sentences with 5, 7 or 12 syllables
def find_alt_forms(st):
    s5 = []; s7 = []; s12 = []
    for sentence in st:
        word_list = syl_count(sentence)
        if word_list != None:
            sylno = sum([w[1] for w in word_list])
            if sylno == 5:
                bs = build_sentence(sentence)
                if bs.count('.,') == 0:
#                     print "(5)", bs
                    s5.append(bs)
            elif sylno == 7:
                bs = build_sentence(sentence)
                if bs.count('.,') == 0:
#                     print "(7)", bs
                    s7.append(bs)
            elif sylno == 12:
                bs = build_sentence(sentence)
                if bs.count('.,') == 0:
#                     print "(12)", bs
                    s12.append(bs)
    return s5, s7, s12

def build_haiku(s5, s7, s12):
    if len(s5) > 1 and len(s7) > 0:
        return s5[0] + "\n", s7[0] + "\n", s5[1]
    if len(s5) > 0 and len(s12) > 0:
        return s12[0] + "\n", s5[0]
    return " "

def build_sentence(words):
    s = " "
    for w in words:
        if w == "$":
            continue
        if not len(w.strip(string.punctuation)):
            if w in ["(", "{", "\{", "[", "`", "``"]:
                s += w
            else:
                s = s[:-1]+w+" "
        else:
            s += w+" "
    s = s.strip()
    s = s[0].upper() + s[1:]
    return s

def load_paper(arxiv_id):
    return arxiv.get_article(arxiv_id)

dfm1 = "1202.3665"
dfm2 = "1310.4179"
dfm4 = "1211.5805"
sk2 = "1207.2945"
sk3 = "1203.5486"
rs2 = "1106.1885"
rs3 = "0807.4382"
bp1 = "1302.6682"
bp2 = "1305.1934"
dh1 = "1008.4686" # haiku
# Data analysis recipes: Fitting a model to data
dfm3 = "1211.6105" # haiku
# The Panchromatic Hubble Andromeda Treasury IV. A Probabilistic Approach to Inferring the High Mass Stellar Initial Mass Function and Other Power-law Functions
dfmra1 = "1309.0654" # haiku
# Maximizing Kepler science return per telemetered pixel: Searching the habitable zones of the brightest stars
fh1 = "1401.6128" # haiku
# The Probabilities of Orbital-Companion Models for Stellar Radial Velocity Data
bs1 = "1211.0278" # haiku
# Moderate-Luminosity Growing Black Holes From 1.25 < z < 2.7: Varied Accretion In Disk-Dominated Hosts
dh2 = "1008.4146"
bp3 = "1401.7566"

st = load_paper(bs1)

print find_haiku(st)
s5, s7, s12 = find_alt_forms(st)
print build_haiku(s5, s7, s12)
