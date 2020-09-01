# from myfuncs import *
import myfuncs

# get keywords, inverted index and titles
f = open('s2-titles.txt', encoding = "utf8")
titles_lines = f.readlines()
f.close()

bag_of_words = myfuncs.get_bag_of_words(titles_lines)
keywords = myfuncs.get_keywords(titles_lines, bag_of_words)
inverted_index = myfuncs.get_inverted_index(keywords)
titles = myfuncs.get_titles(titles_lines)

# run search query
query = input('Input your search query: ')
while query != '':
    query_terms = query.split()
    sorted_results = myfuncs.get_search_results(query_terms,
                                        keywords,
                                        inverted_index)
    print('==> search results for query:', query)
    for result in sorted_results:
        print(result, titles[result])
    query = input('Input your search query [hit return to finish]: ')

# get unit vectors
f = open('s2-categories.tsv', encoding = "utf8")
categories_lines = f.readlines()
f.close()
unit_vectors = myfuncs.get_unit_vectors(keywords, categories_lines)

# run recommendation algorithm
seed_courseid = input('Input your seed courseid: ')
while seed_courseid != '':
    sorted_results = myfuncs.get_recommendation_results(seed_courseid,
                                                keywords,
                                                inverted_index,
                                                unit_vectors)
    print('==> recommendation results:')
    for result in sorted_results:
        print(result, titles[result])
        print(myfuncs.get_dot_product(seed_courseid, result, unit_vectors))
    seed_courseid = input("Input seed courseid [hit return to finish]: ")

