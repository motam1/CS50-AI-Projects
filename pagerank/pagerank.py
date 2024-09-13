import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    links = corpus[page]
    total_pages = len(corpus)
    total_links = len(links)
    dictionary = {}

    for page in corpus:
        dictionary[page] = 0
    
    # If there are no links, all pages have equal probability
    if len(links) == 0:
        for page in corpus:
            dictionary[page] = 1/total_pages
        return dictionary

    # Adding probability if a page is linked
    for link in links:
        dictionary[link] = damping_factor/total_links

    # Added probability created by the damping factor
    added_prob = (1-damping_factor)/total_pages
    for page in corpus:
        dictionary[page] += added_prob
    
    return dictionary

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dictionary = {}
    for page in corpus:
        dictionary[page] = 0
    
    # Randomly selecting the first page
    curr_sample = random.choice(list(corpus.keys()))

    # Sampling n pages using transition model
    for sample in range(n):
        dictionary[curr_sample] += (1/n)
        next_sample_probs = transition_model(corpus, curr_sample, damping_factor)
        next_sample = random.choices(list(next_sample_probs), k = 1, weights = next_sample_probs.values())[0]
        curr_sample = next_sample
    
    return dictionary    
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dictionary = {}
    
    total_pages = len(corpus)

    # Assigning initial pageranks of 1/N
    for page in corpus:
        dictionary[page] = 1/total_pages
    
    # Loops until condition (convergence of pageranks) is met
    while 1:
        update_dict = {}
        for page in corpus:
            #Perform PR(p) calculation
            update_dict[page] = (1 - damping_factor)/total_pages
            for i in corpus:
                if page in corpus[i]:
                    update_dict[page] += damping_factor * (dictionary[i]/len(corpus[i]))
                #If the page has no links, treat as if it links all pages
                if (len(corpus[i])) == 0:
                    update_dict[page] += damping_factor * (dictionary[i]/total_pages)
        
        # Checks convergence
        complete = True
        for page in corpus:
            if abs(dictionary[page] - update_dict[page]) > 0.001:
                complete = False
        dictionary = update_dict
        if complete:
            return dictionary
             
    raise NotImplementedError


if __name__ == "__main__":
    main()
