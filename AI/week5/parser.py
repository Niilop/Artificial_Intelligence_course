import argparse

import nltk
import sys
import re

from nltk import word_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V | NP VP | NP VP Conj NP VP
PP -> P | P N | P NP 
VP -> V | V NP | VP PP | Adv V | Adv V NP | Adv VP PP | V Adv
NP -> N | Det N | Det Adj N | Det Adj Adj N | Det Adj Adj Adj N | NP PP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('directory', help="load the data files from this directory", nargs="?")
    arg_parser.add_argument("-q", "--quiet", help="print just the noun phrase chunks (used by the grader)",
                            action="store_true")
    args = arg_parser.parse_args()

    # If filename specified, read sentence from file
    if args.directory is not None:
        with open(args.directory) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    if not args.quiet:
        for tree in trees:
            tree.pretty_print()

            print("Noun Phrase Chunks")
            for np in np_chunk(tree):
                print(" ".join(np.flatten()))

    # Print just the noun phrase chunks
    else:
        np_set = set()
        for tree in trees:
            for np in np_chunk(tree):
                np_set.add(" ".join(np.flatten()))

        print("Noun Phrase Chunks")
        for np in sorted(np_set):
            print(np)


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    sentence = sentence.split()
    words = []
    for word in sentence:
        cleaned = ""
        for letter in word:

             if letter.isalpha():
                 cleaned += letter.lower()
        if cleaned:
            words.append(cleaned)
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    noun_phrases = []

    for t in tree:
        for subtree in t.subtrees():
            if subtree.label() == 'NP':
                is_np = True

                for subcheck in subtree:

                    if type(subcheck) != str:
                        if subcheck.label() == 'PP' or subcheck.label() == 'NP':
                            is_np = False
                if (is_np):
                    noun_phrases.append(subtree)


    return noun_phrases

if __name__ == "__main__":
    main()
