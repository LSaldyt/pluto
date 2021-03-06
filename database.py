#!/usr/bin/env python3
from collections import defaultdict
from pprint import pprint

def _frontchains(chain):
    for i in range(1, len(chain) + 1):
        yield tuple(chain[:i])

def _subchains(chain):
    if len(chain) == 1:
        return []
    else:
        first, *remaining = chain
        return list(_frontchains(chain)) + [tuple(remaining)] + _subchains(remaining)

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

    def _get_level_key(self, *values):
        assert len(values) > 1, 'Cannot insert without at least one key and one value'
        keychain = values[:-1]
        value    = values[-1]

        for subchain in _subchains(values):
            self.mentions[subchain].add(tuple(keychain))

        level = self.entries
        for key in keychain[:-1]:
            if key not in level:
                level[key] = dict()
            elif not isinstance(level[key], dict):
                raise ValueError('Cannot insert past already-terminal keychain: {}'.format(key))
            level = level[key]
        key = keychain[-1]
        return level, key

    def _insert(self, *values):
        level, key = self._get_level_key(*values)
        level[key] = values[-1]

    def clear(self, string):
        level, key = self._get_level_key(*string.split())
        level[key] = dict()
        print('Cleared {}'.format(string))

    def add(self, string):
        self._insert(*string.split(' '))
        print('Added {}'.format(string))

    def get(self, string):
        print('Getting {}'.format(string))
        print(self._mentions(*string.split(' ')))
        return self._mentions(*string.split(' '))

    def find(self, string, filt=None):
        print('Finding {}'.format(string))
        sets = [self._mentions(*s.strip().split(' ')) for s in string.split(',')] 
        sets = [{keychain[0] for keychain in mentions} for mentions in sets] 
        found = set.intersection(*sets)
        print(found)
        if filt is not None:
            found = {item for item in found if filt(item)}
        return found

    def select(self, string):
        result = self.find(string)
        if len(result) != 1:
            raise ValueError('Query "{}" could not be resolved'.format(string))
        return list(result)[0]

    def view(self):
        print('Viewing database:')
        pprint(self.entries)
