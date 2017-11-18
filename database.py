#!/usr/bin/env python3
from collections import defaultdict

class Database(object):
    def __init__(self):
        self.entries  = dict()
        self.mentions = defaultdict(set)

    def _lookup(self, keychain):
        level = self.entries
        for key in keychain:
            if key not in level:
                raise KeyError('{} not in level'.format(key))
            else:
                level = level[key]
        return level

    def _mentions(self, *keys):
        return self.mentions[tuple(keys)]

    def _insert(self, *values):
        assert len(values) > 1, 'Cannot insert without at least one key and one value'
        keychain = values[:-1]
        value    = values[-1]

        self.mentions[(value,)].add(tuple(keychain))

        for i in range(1, len(values) + 1):
            subchain = values[:i]
            self.mentions[tuple(subchain)].add(tuple(keychain))

        for i in range(1, len(values)):
            subchain = values[i:]
            self.mentions[tuple(subchain)].add(tuple(keychain))
        
        for key in keychain:
            self.mentions[(key,)].add(tuple(keychain))

        level = self.entries
        for key in keychain[:-1]:
            if key not in level:
                level[key] = dict()
            elif not isinstance(level[key], dict):
                raise ValueError('Cannot insert past already-terminal keychain: {}'.format(key))
            level = level[key]
        key = keychain[-1]
        level[key] = value

    def add(self, string):
        self._insert(*string.split(' '))
        print('Added {}'.format(string))

    def get(self, string):
        print(self._mentions(*string.split(' ')))
