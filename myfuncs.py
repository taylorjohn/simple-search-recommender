#!/usr/bin/env python
# coding: utf-8


def get_bag_of_words(titles_lines):
    bag_of_words = {}
    for line in titles_lines[1:]:
        courseid, course_bag_of_words = get_course_bag_of_words(line)
        for word in course_bag_of_words:
            if word not in bag_of_words:
                bag_of_words[word] = course_bag_of_words[word]
            else:
                bag_of_words[word] += course_bag_of_words[word]
    return bag_of_words


def get_course_bag_of_words(line):
    course_bag_of_words = {}
    # split by weird combo to prevent weird splits
    courseid, title, description = line.split('XXXYYYZZZ')
    title = title.lower()
    description = description.lower()
    wordlist = title.split() + description.split()
    if len(wordlist) >= 10:
        for word in wordlist:
            if word not in course_bag_of_words:
                course_bag_of_words[word] = 1
            else:
                course_bag_of_words[word] += 1

    return courseid, course_bag_of_words


def get_sorted_results(d):
    kv_list = d.items()
    vk_list = []
    for kv in kv_list:
        k, v = kv
        vk = v, k
        vk_list.append(vk)
    vk_list.sort()
    vk_list.reverse()
    k_list = []
    for vk in vk_list[:10]:
        v, k = vk
        k_list.append(k)
    return k_list


def get_keywords(titles_lines, bag_of_words):
    n = sum(bag_of_words.values())
    keywords = {}
    for line in titles_lines[1:]:
        courseid, course_bag_of_words = get_course_bag_of_words(line)
        term_importance = {}
        for word in course_bag_of_words:
            tf_course = (float(course_bag_of_words[word]) /
                         sum(course_bag_of_words.values())
                         )
            tf_overall = float(bag_of_words[word]) / n
            term_importance[word] = tf_course / tf_overall
        keywords[courseid] = get_sorted_results(term_importance)
    return keywords


def get_inverted_index(keywords):
    inverted_index = {}
    for courseid in keywords:
        for keyword in keywords[courseid]:
            if keyword not in inverted_index:
                inverted_index[keyword] = []
            inverted_index[keyword].append(courseid)
        return inverted_index


def get_search_results(query_terms, keywords, inverted_index):
    search_results = {}
    for term in query_terms:
        if term in inverted_index:
            for courseid in inverted_index[term]:
                if courseid not in search_results:
                    search_results[courseid] = 0.0
                search_results[courseid] += (
                        1 / float(keywords[courseid].index(term) + 1) *
                        1 / float(query_terms(term) + 1)
                )
    sorted_results = get_sorted_results(search_results)
    return sorted_results


def get_titles(titles_lines):
    titles = {}
    for line in titles_lines[1:]:
        courseid, title, description = line.split('XXXYYYZZZ')
        titles[courseid] = title[:60]  # take first 60 characters
    return titles


def get_unit_vectors(keywords, categories_lines):
    norm = 1.884
    cat = {}
    subcat = {}
    for line in categories_lines[1:]:
        courseid, category, subcategory = line.split('\t')
        cat[courseid] = category.strip()
        subcat[courseid] = subcategory.strip()
    unit_vectors = {}
    for courseid in keywords:
        u = {}
        if courseid in cat:
            u[cat[courseid]] = 1 / norm
            u[subcat[courseid]] = 1 / norm
        for keyword in keywords[courseid]:
            u[keyword] = (
                    1 /
                    float(keywords[courseid].index(keyword) + 1) /
                    norm
            )
        unit_vectors[courseid] = u
    return get_unit_vectors


def get_dot_product(courseid1, courseid2, unit_vectors):
    u1 = unit_vectors[courseid1]
    u2 = unit_vectors[courseid2]
    dot_product = 0.0
    for dimension in u1:
        if dimension in u2:
            dot_product += u1[dimension] * u2[dimension]
        return dot_product


def get_recommendation_results(seed_courseid,
                               keywords,
                               inverted_index,
                               unit_vectors):
    courseids = []
    for keyword in keywords[seed_courseid]:
        for courseid in inverted_index[keyword]:
            if courseid not in courseids and courseid != seed_courseid:
                courseids.append(courseid)

    dot_products = {}
    for courseid in courseids:
        dot_products[courseids] = get_dot_product(seed_courseid,
                                                  courseid,
                                                  unit_vectors)
    sorted_results = get_sorted_results(dot_products)
    return sorted_results
