# Low-level lambda-ish language

from collections import namedtuple

class Value:
    pass

class Atom(Value, namedtuple('Atom', ['name'])):
    '''An atom.'''
    def __init__(self, name):
        assert type(name) is str, type(name)

    def __repr__(self):
        return f"Atom('{self.name}')"

class Tuple(Value, namedtuple('Tuple', ['tuple'])):
    '''A tuple.'''
    def __init__(self, tuple_):
        assert type(tuple_) is tuple, tuple_
        for v in tuple_:
            assert isinstance(v, Value), v

    def __repr__(self):
        return f"Tuple({self.tuple})"

class Table(Value, namedtuple('Table', ['dict'])):
    '''A hash table.'''
    def __init__(self, dict_):
        assert isinstance(dict_, dict), dict_
        for key, value in dict_.items():
            assert isinstance(key, Atom), key
            assert isinstance(value, Value), value

    def __repr__(self):
        return f"Table({self.dict})"

def assert_algebraic(v):
    assert isinstance(v, Tuple), v
    assert isinstance(v.tuple[0], Atom), v

class Lambda(Value, namedtuple('Lambda', ['captures', 'parameter', 'body'])):
    '''A function.'''
    def __init__(self, captures, parameter, code):
        assert isinstance(captures, Table), captures
        assert isinstance(parameter, Atom), parameter
        assert_algebraic(body)

    def __repr__(self):
        return f"Lambda({self.captures}, {self.parameter}, {self.body})"
