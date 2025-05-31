from itertools import groupby, permutations
import math
from collections import Counter
# https: // github.com/ricea/yizhen-step-repo/tree/office-hours-1/week1
# https: // docs.google.com/document/d/19ZGJwsQ0qxx2hiqqKxR4trSIznq07OT1Xc-0yBdu0LQ/edit?tab = t.0
# ----------------------------------------
# | 1 point  | a, e, h, i, n, o, r, s, t |
# | 2 points | c, d, l, m, u             |
# | 3 points | b, f, g, p, v, w, y       |
# | 4 points | j, k, q, x, z             |
# ----------------------------------------
SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2,
          2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
INPUTS = ['./input/small.txt', './input/medium.txt', './input/large.txt']
OUTPUTS = ['./output/small.txt', './output/medium.txt', './output/large.txt']


class AnagramSubstr:
    '''
        input: a random str
        search word from dictionary
        can set substr length
        map chars into calculate table

        method 1: choose permutation substrs from input, search all permutations
        method 2: count input and dict, search subset (get all anagrams)
    '''

    def __init__(self) -> None:
        self.dictionary = self.group_dictionary(self.sort_dictionary())
        self.accounted_dictionary = self.account_dictionary(self.dictionary)

    def find_highest_score(self, words: list[str]) -> str:
        highest_score = -1
        word_with_highest_score = ''

        for word in words:
            current_score = 0
            for char in word:
                current_score += ord(char)-ord('a')
            if current_score >= highest_score:
                highest_score = current_score
                word_with_highest_score = word
        return word_with_highest_score

# -------------------------find_anagram_with_combination-------------------------

    def find_anagram_with_combination(self, str: str) -> list[str]:
        '''method 1: choose substrs from input, search all (works the same as 1.py)'''
        str_sorted = ''.join(sorted(str))
        substrs = self.find_combination(str_sorted)
        result = []
        for substr in substrs:
            anagram = self.binary_search(substr)
            result.extend(anagram)
        return result

    def find_combination(self, str: str) -> list[str]:
        result = ['']
        for i in range(0, len(str)):
            l = len(result)
            for j in range(0, l):
                result.append(result[j]+str[i])

        return result

    def binary_search(self, str: str) -> list[str]:
        left = 0
        right = len(self.dictionary)
        mid = math.floor((0+right)/2
                         )
        while (left <= right):
            mid_word = self.dictionary[mid][0]
            if (mid_word == str):
                return self.dictionary[mid][1]
            if (mid_word < str):
                left = mid+1
                mid = math.floor((left+right)/2)
            else:
                right = mid-1
                mid = math.floor((left+right)/2)
        return []
# -------------------------Finish of find_anagram_with_combination-------------------------

# -------------------------find_anagram_with_account_char-------------------------

    def find_anagram_with_account_char(self, str: str) -> list[str]:
        '''method 2: count input and dictionary, search subset(get all anagrams)'''
        accounted_str = dict(Counter(sorted(str)))
        result = self.search_subset(accounted_str)
        return result

    def search_subset(self, accounted_str: dict[str, int]) -> list[str]:
        result = []
        for word, word_list in self.accounted_dictionary:
            if self.check_is_substr(word, accounted_str):
                result.extend(word_list)
        return result

    def check_is_substr(self, word: dict[str, int], accounted_str: dict[str, int]) -> bool:
        for key, value in word.items():
            if key not in accounted_str or accounted_str[key] < value:
                return False
        return True

# -------------------------Finish of find_anagram_with_account_char-------------------------

# -------------------------prepare dictionary-------------------------

    def sort_dictionary(self) -> list[tuple[str, str]]:
        '''
        sort words.txt
        return a list of ('sorted_word, origin_word)
        '''
        with open('./words.txt', 'r') as file:
            content = file.read().splitlines()
            pair_dictionary = list(
                map(lambda s: (''.join(sorted(s)), s), content))
            sorted_dictionary = sorted(
                pair_dictionary, key=lambda tuple: tuple[0])
            return sorted_dictionary

    def group_dictionary(self, dictionary: list[tuple[str, str]]) -> list[tuple[str, list[str]]]:
        '''groupby: returns a iterator of (sharing_key, a_iterator_of_origin_values)
            the sharing_key can be customized
            we need to extract the origin_word from a_iterator_of_origin_values, which is composed of(sorted_word, orgiin_word)
        '''
        group = groupby(dictionary, key=lambda tuple: tuple[0])
        # g: a iterator of (sorted_word, orgiin_word)
        grouped_dictionary = [(k, [tuple[1]for tuple in g]) for k, g in group]
        return grouped_dictionary

    def account_dictionary(self, dictionary: list[tuple[str, list[str]]]) -> list[tuple[dict[str, int], list[str]]]:
        accounted_dictionary = [(dict(Counter(word)), word_list)
                                for word, word_list in dictionary]
        return accounted_dictionary

# -------------------------Finish of prepare dictionary-------------------------
# -------------------------driver code for read / write file-------------------------

    def input_from_file(self, path: str) -> list[str]:
        result = []
        with open(path) as file:
            input = file.read().splitlines()
            for word in input:
                anagrams = self.find_anagram_with_account_char(word)
                anagram_with_highest_score = self.find_highest_score(anagrams)
                result.append(anagram_with_highest_score)
        print(result)
        return result

    def output_to_file(self, words: list, path: str) -> None:
        with open(path, 'w') as file:
            for word in words:
                file.writelines(f'{word}\n')


anagram = AnagramSubstr()
# anagram.find_anagram_with_combination('')
for i in range(len(INPUTS)):
    res = anagram.input_from_file(INPUTS[i])
    anagram.output_to_file(res, OUTPUTS[i])
