'''
Constructs wobject code values.
'''

from collections import OrderedDict

import model

class Environment:
    '''
    Represents a mapping from names to their meanings.
     - constant - function from str to optional Value.
     - free_variables - mutable set of str.
    '''
    def __init__(self, constant=lambda name: None, free_variables=None):
        self.constant = constant
        self.free_variables = free_variables or set()

    def __repr__(self):
        return f"Environment(free_variables={self.free_variables})"

    def compile(self, name_):
        assert type(name_) is str
        value = self.constant(name)
        if value is not None:
            return constant(name_, value)
        self.free_variables.add(name_)
        return name(name_)

# Atoms used to tag expressions.
CONSTANT = model.Atom('Constant')
TUPLE = model.Atom('Tuple')
TABLE = model.Atom('Table')
LAMBDA = model.Atom('Lambda')
APPLY = model.Atom('Apply')
NAME = model.Atom('Name')

def constant(name, value):
    '''
     - name - str (for debugging only).
     - value - Value.
    '''
    return model.Tuple((CONSTANT, model.Atom(name), value))

def tuple_(iterable):
    '''
     - values - iterable of Value.
    '''
    values = model.Tuple(tuple(iterable))
    return model.Tuple((TUPLE, values))

def table(iterable):
    '''
     - entries - iterable of (str, Value).
    '''
    entries = model.Table({
        model.Atom(name): value
        for name, value in iterable
    })
    return model.Tuple((TABLE, entries))

def lambda_(captures, parameter, body):
    '''
     - captures - iterable of (str, Value).
     - parameter - str.
     - body - algebraic Value.
    '''
    captures = model.Table(captures)
    parameter = model.Atom(parameter)
    model.assert_algebraic(body)
    return model.Tuple((LAMBDA, captures, parameter, body))

def name(name):
    '''
     - name - str.
    '''
    return model.Tuple((NAME, model.Atom(name)))

def atom(name):
    '''
     - name - str.
    '''
    return constant(name, model.Atom(name))
