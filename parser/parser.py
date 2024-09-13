import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
import sys

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
S -> NP VP | S Conj S
AP -> Adj | Adj AP
NP -> N | Det NP | AP NP | N PP | NP Conj NP
PP -> P NP
VP -> V | V NP | V NP PP | V PP | VP Conj VP | Aux VP | VP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
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
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    word_list = []
    
    # Convert sentence to lowercase and tokenize
    sentence = sentence.lower()
    sentence = nltk.word_tokenize(sentence)
    
    # Iterate through each token in the sentence
    for token in sentence:
        letter = False
        # If the token contrains a character from the alphabet, append to word list 
        for char in token:
            if char.isalpha():
                letter = True
        if letter == True:
            word_list.append(token)

    return word_list
   


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_list = []
    # Iterate through each subtree with label 'NP'
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            # If the subtree does not contain its own subtree with label 'NP', append to list
            np_within = False
            for within in subtree.subtrees():
                if within.label() == 'NP' and within != subtree:
                    np_within = True
            if np_within == False:
                np_list.append(subtree)

    return np_list


if __name__ == "__main__":
    main()
