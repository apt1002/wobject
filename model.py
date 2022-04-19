# Low-level lambda-ish language

from collections import namedtuple

class WError(Exception):
    pass

def error(message):
    raise WError(message)

class Value:
    pass

class Atom(Value, namedtuple('Atom', ['name'])):
    '''An atom.'''
    def __init__(self, name):
        assert type(name) is str, type(name)

    def __repr__(self):
        return f"Atom('{self.name}')"

class Table(Value, namedtuple('Table', ['dict'])):
    '''A hash table.'''
    def __init__(self, dict_):
        assert isinstance(dict_, dict), dict_
        for key, value in dict_.items():
            assert isinstance(key, str), key
            assert isinstance(value, Value), value

    def __repr__(self):
        return f"Table({self.dict})"

class Lambda(Value, namedtuple('Lambda', ['captures', 'parameter', 'body'])):
    '''A function.'''
    def __init__(self, captures, parameter, body):
        assert isinstance(captures, dict), captures
        assert isinstance(parameter, str), parameter
        assert isinstance(body, Table), body

    def __repr__(self):
        return f"Lambda({self.captures}, {self.parameter}, {self.body})"

NULL = Atom('')
