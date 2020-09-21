#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Michael Trepanier"


import cProfile
import pstats
import timeit
from collections import Counter
duplicates = []


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    def wrapper(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()
        result = func(*args, **kwargs)
        profile.disable()
        profilestats = pstats.Stats(profile).sort_stats("cumulative")
        profilestats.print_stats()
        return result
    return wrapper


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    # Not optimized
    movies = read_movies(src)
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)

#
# Students: write a better version of find_duplicate_movies
#


def optimized_find_duplicate_movies(src):
    movies = read_movies(src)
    movies_Counter = Counter()
    for movie in movies:
        movies_Counter[movie] += 1
    duplicates = [movie for movie, V in movies_Counter.items() if V > 1]
    return duplicates


# def wrapper(func, *args, **kwargs):
#     def wrapped():
#         return func(*args, **kwargs)
#     return wrapped


def timeit_helper(func_name, func_params):
    """Part A: Obtain some profiling measurements using timeit"""
    assert isinstance(func_name, str)
    setup = """
from __main__ import find_duplicate_movies
src = "movies.txt"
    """
    # setup += f"src={func_params}"

    # wrapped = wrapper(func_name, func_params)
    # statement = func_name + "(" + ")"
    t = timeit.Timer(stmt="print(type(d))", setup="d = []")
    runs_per_repeat = 3
    num_repeats = 5
    result = t.repeat(repeat=num_repeats, number=runs_per_repeat)
    # print(result)
    # avg = map(lambda x: x/3, result)
    # min_list = list(avg)
    time_cost = min(result)/(num_repeats)

    print(f"func={func_name}  num_repeats={num_repeats} \
    runs_per_repeat={runs_per_repeat} time_cost={time_cost} sec")
    return t


def main():
    """Computes a list of duplicate movie entries."""
    # Students should not run two profiling functions at the same time,
    # e.g. they should not be running 'timeit' on a function that is
    # already decorated with @profile

    filename = 'movies.txt'

    print("--- Before optimization ---")
    timeit_helper("find_duplicate_movies", filename)
    print(f'Found {len(duplicates)} duplicate movies:')
    print('\n'.join(duplicates))

    print("\n--- cProfile results, before optimization ---")
    profile(find_duplicate_movies)(filename)

    print("\n--- cProfile results, after optimization ---")
    profile(optimized_find_duplicate_movies)(filename)


if __name__ == '__main__':
    # import timeit
    main()
    print("Completed.")
