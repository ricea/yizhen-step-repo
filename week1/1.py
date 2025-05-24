from itertools import groupby
import math


class Anagram:
    '''
    input: a random str
    search word from dictionary
    find all, like pssu -> puss, sups
    '''

    def __init__(self) -> None:
        self.dictionary = self.group_dictionary(self.sort_dictionary())

    def find_anagram(self, str: str) -> list[str]:
        '''return all anagrams found'''
        str_sorted = ''.join(sorted(str))
        # Sort input, sort dictionary
        # O(n*logn)
        result = self.binary_search(str_sorted)
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


anagram = Anagram()
result = []
with open('./input/test.txt') as file:
    inputs = file.read().splitlines()
    print(inputs)
    for str in inputs:
        result.append(anagram.find_anagram(str))

print(result)
