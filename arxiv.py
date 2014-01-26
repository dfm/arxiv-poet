#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["get_article"]

import os
import gzip
import tarfile
import requests
import tempfile
import subprocess
from bs4 import BeautifulSoup

from nltk import sent_tokenize, word_tokenize


DATA_DIR = "data"


def clean_word(w):
    return w.strip("$*")


def parse_tex(tex):
    # Use pandoc to convert .tex to .html
    with tempfile.NamedTemporaryFile(suffix=".tex") as tex_f:
        tex_f.write(tex)
        tex_f.flush()
        with tempfile.NamedTemporaryFile(suffix=".html") as txt_f:
            subprocess.check_call(["pandoc", tex_f.name, "-o", txt_f.name])
            body = txt_f.read().decode("utf-8")

    # Parse the HTML.
    tree = BeautifulSoup(body)
    paragraphs = []
    for p in tree.find_all("p"):
        txt = p.text
        if not len(txt):
            continue
        paragraphs.append(map(word_tokenize, sent_tokenize(txt)))

    return [[w for w in map(clean_word, s) if len(w)]
            for p in paragraphs for s in p if len(s)]


def get_article(arxiv_id, clobber=False):
    # Try to load cached file.
    fn = "{0}.tar.gz".format(arxiv_id)
    local = os.path.join(DATA_DIR, fn)

    # Download the remote file.
    if clobber or not os.path.exists(local):
        url = "http://arxiv.org/e-print/{0}".format(arxiv_id)
        r = requests.get(url)
        code = r.status_code
        if code != requests.codes.ok:
            print("Download of {0} failed with code: {1}".format(url, code))
            return None
        with open(local, "wb") as f:
            f.write(r.content)

    # Parse the tex files in the archive.
    tex = []
    if tarfile.is_tarfile(local):
        with tarfile.open(local) as f:
            for member in f:
                if os.path.splitext(member.name)[1] == ".tex":
                    tex.append(f.extractfile(member).read())
    else:
        with gzip.open(local) as f:
            tex.append(f.read())

    print("Found {0} tex file(s)".format(len(tex)))

    return [s for p in map(parse_tex, tex) for s in p if len(s)]


if __name__ == "__main__":
    import sys
    aid = "1309.0653"
    if len(sys.argv) > 1:
        aid = sys.argv[1]
    print("\n".join(map(" ".join, get_article(aid))).encode("utf-8"))
