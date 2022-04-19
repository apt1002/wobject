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
        value = self.constant(name_)
        if value is not None:
            return constant(name_, value)
        self.free_variables.add(name_)
        return name(name_)

def name(name):
    '''
     - name - str.
    '''
    return model.Table({
        '': model.Atom('name'),
        'name': model.Atom(name),
    })

def lambda_(captures, parameter, body):
    '''
     - captures - iterable of (str, Value).
     - parameter - str.
     - body - Table - compiled code.
    '''
    assert type(body) is model.Table
    return model.Table({
        '': model.Atom('lambda'),
        'captures': model.Table(dict(captures)),
        'parameter': model.Atom(parameter),
        'body': body,
    })

def apply(function, argument):
    '''
     - function - Value.
     - argument - Value.
    '''
    return model.Table({
        '': model.Atom('apply'),
        'function': function,
        'argument': argument,
    })

def table(iterable):
    '''
     - entries - iterable of (str, Value).
    '''
    return model.Table({
        '': model.Atom('table'),
        'table': model.Table(dict(iterable)),
    })

def constant(name, value):
    '''
     - name - str (for debugging only).
     - value - Value.
    '''
    return model.Table({
        '': model.Atom('constant'),
        'constant': value,
        'debug': model.Atom(name),
    })

def atom(name):
    '''
     - name - str.
    '''
    return model.Table({
        '': model.Atom('constant'),
        'constant': model.Atom(name),
    })
