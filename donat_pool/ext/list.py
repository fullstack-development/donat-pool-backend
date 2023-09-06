import itertools

def map_by_list(f, l):
    return list(map(f, l))

def clean_list(l):
    return list(itertools.filterfalse(lambda item: not item , l))