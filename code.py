'''
Constructs wobject code values. Code is represented by a `Table` with key `''`.
'''

from typing import Optional, Set, Callable, Tuple, Iterable
from collections import OrderedDict

import model
from model import Value, Atom, Table

class Environment:
    '''
    Represents a mapping from names to their meanings.
     - free_variables - mutable set of str. Updated by `compile()`.
    '''
    def __init__(self,
        constant: Callable[[str], Optional[Value]] = lambda name: None,
        free_variables: Optional[Set[str]] = None,
    ) -> None:
        self.constant = constant
        self.free_variables = free_variables or set()

    def __repr__(self) -> str:
        return f"Environment(free_variables={self.free_variables})"

    def compile(self, name_: str) -> Table:
        value = self.constant(name_)
        if value is not None:
            return constant(name_, value)
        self.free_variables.add(name_)
        return name(name_)

def name(name: str) -> Table:
    return Table({
        '': Atom('name'),
        'name': Atom(name),
    })

def lambda_(captures: Iterable[Tuple[str, Value]], parameter: str, body: Table) -> Table:
    assert type(body) is Table
    captures_dict = dict(captures)
    assert parameter not in captures_dict, (parameter, captures_dict)
    return Table({
        '': Atom('lambda'),
        'captures': Table(captures_dict),
        'parameter': Atom(parameter),
        'body': body,
    })

def apply(function: Table, argument: Table) -> Table:
    return Table({
        '': Atom('apply'),
        'function': function,
        'argument': argument,
    })

def table(iterable: Iterable[Tuple[str, Value]]) -> Table:
    return Table({
        '': Atom('table'),
        'table': Table(dict(iterable)),
    })

def constant(name: str, value: Value) -> Table:
    '''
     - name - str (for debugging only).
    '''
    return Table({
        '': Atom('constant'),
        'constant': value,
        'debug': Atom(name),
    })

def atom(name: str) -> Table:
    return Table({
        '': Atom('constant'),
        'constant': Atom(name),
    })
