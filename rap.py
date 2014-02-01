from nltk.corpus import cmudict
import nltk
import string
import numpy as np
import arxiv
import haiku

def load_paper(arxiv_id):
    return arxiv.get_article(arxiv_id)

ph = cmudict.dict()

# Find a list of rhyming sentences
def algorhyme(st):
    lst2 = []
    words = []
    rhyme_list = []
    for sentence in st:
        word_list = haiku.syl_count(sentence)
        if word_list == None:
            words.append('blah')
            blank = ['0', '0']
            lst2.append(blank)
        else:
            words.append(word_list[-1][0])
            phonemes = ph[word_list[-1][0].lower()][0]
            lst2.append(phonemes[-2:])
    for i in range(len(lst2)):
        for j in range(len(lst2)):
            rhymes = []
            if lst2[i] != blank and lst2 != blank:
                if lst2[i] == lst2[j]:
                    if words[i] != words[j]:
                        rhymes.append(haiku.build_sentence(st[i]))
                        rhymes.append(haiku.build_sentence(st[j]))
                        rhyme_list.append(rhymes)
    return rhyme_list

dh1 = "1008.4686"
dh2 = "1008.4146"
st = load_paper(dh1)
st.extend(load_paper(dh2))
rhyme_list = algorhyme(st)
# print len(rhyme_list), "rhymes found"

# for i in rhyme_list:
#     print i
#     raw_input('enter')
