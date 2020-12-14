import re
from collections import Counter
import numpy as np
import pandas as pd


def get_count(word_l):

    word_count_dict = {}
    word_count_dict = Counter(word_l)
    return word_count_dict


def get_probs(word_count_dict):

    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs


def delete_letter(word, verbose=False):

    delete_l = []
    split_l = []

    for c in range(len(word)):
        split_l.append((word[:c], word[c:]))
    for a, b in split_l:
        delete_l.append(a + b[1:])

    if verbose: print(f"input word {word}, \nsplit_l = {split_l}, \ndelete_l = {delete_l}")

    return delete_l


def switch_letter(word, verbose=False):

    def swap(c, i, j):
        c = list(c)
        c[i], c[j] = c[j], c[i]
        return ''.join(c)

    switch_l = []
    split_l = []
    len_word = len(word)
    for c in range(len_word):
        split_l.append((word[:c], word[c:]))
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_l if len(b) >= 2]

    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nswitch_l = {switch_l}")

    return switch_l


def replace_letter(word, verbose=False):

    letters = 'abcdefghijklmnopqrstuvwxyz'
    replace_l = []
    split_l = []

    for c in range(len(word)):
        split_l.append((word[0:c], word[c:]))
    replace_l = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_l if b for l in letters]
    replace_set = set(replace_l)
    replace_set.remove(word)
    replace_l = sorted(list(replace_set))

    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nreplace_l {replace_l}")

    return replace_l


def insert_letter(word, verbose=False):

    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_l = []
    split_l = []
    for c in range(len(word) + 1):
        split_l.append((word[0:c], word[c:]))
    insert_l = [a + l + b for a, b in split_l for l in letters]

    if verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")

    return insert_l


def edit_one_letter(word, allow_switches=True):

    edit_one_set = set()
    edit_one_set.update(delete_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))

    return edit_one_set


def edit_two_letters(word, allow_switches=True):

    edit_two_set = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w, allow_switches=allow_switches)
            edit_two_set.update(edit_two)

    return edit_two_set


def get_corrections(word, probs, vocab, n=2, verbose=False):

    suggestions = []
    n_best = []
    suggestions = list(
        (word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(
            vocab))
    n_best = [[s, probs[s]] for s in list(reversed(suggestions))]
    if verbose: print("suggestions = ", suggestions)

    return n_best


cleaned_data = pd.read_csv("cleaned_dataset (1).csv")
word_l = [ word for sentence in cleaned_data["text"] for word in sentence.split()]
vocab = set(word_l)
word_count_dict = get_count(word_l)
probs = get_probs(word_count_dict)
my_word = 'alawy'
tmp_corrections = get_corrections(my_word, probs, vocab, 2)
for i, word_prob in enumerate(tmp_corrections):
    print(f"word {i}: {word_prob[0]}, prob =  {word_prob[1]:.6f}")
