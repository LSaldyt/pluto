#!/usr/bin/env python3
from collections import defaultdict

def _keychain_lookup(level, keychain):
    for key in keychain:
        if key not in level:
            raise KeyError('{} not in level'.format(key))
        else:
            level = level[key]
    return level

class MultiDictionary(object):

    def __init__(self):
        self.entries  = dict()
        self.reverse  = defaultdict(list)
        self.mentions = defaultdict(list)

    def lookup(self, keychain):
        return _keychain_lookup(self.entries, keychain)

    def reverse_lookup(self, value):
        return self.reverse[value]

    def keychain_mentions(self, *keys):
        return self.mentions[tuple(keys)]

    def insert(self, *values):
        assert len(values) > 1, 'Cannot insert without at least one key and one value'
        keychain = values[:-1]
        value    = values[-1]

        self.reverse[value].append(tuple(keychain))

        for i in range(1, len(keychain) + 1):
            subchain = keychain[:i]
            self.mentions[tuple(subchain)].append(tuple(keychain))

        for i in range(len(keychain)):
            subchain = keychain[i:]
            self.mentions[tuple(subchain)].append(tuple(keychain))
        
        for key in keychain:
            self.mentions[(key,)].append(tuple(keychain))

        level = self.entries
        for key in keychain[:-1]:
            if key not in level:
                level[key] = dict()
            elif not isinstance(level[key], dict):
                raise ValueError('Cannot insert past already-terminal keychain: {}'.format(key))
            level = level[key]
        key = keychain[-1]
        level[key] = value

if __name__ == '__main__':
    mdict = MultiDictionary()
    mdict.insert('a', 'b', 'c', 'd', 'e')
    mdict.insert('a', 'b', 'c', 'f', 'e')

    print(mdict.reverse_lookup('e'))
    print(mdict.keychain_mentions('b'))
    print(mdict.keychain_mentions('a', 'b'))
    print(mdict.keychain_mentions('c', 'd'))
