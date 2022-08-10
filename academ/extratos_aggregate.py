"""
Library to aggregate students data
"""
from collections import Counter
from itertools import chain

def Count_subjects_demand(subject_demand_list):
    return Counter(chain.from_iterable(subject_demand_list)).most_common()
