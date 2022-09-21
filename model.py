# Low-level lambda-ish language

from typing import Dict, NoReturn
from collections import namedtuple

class WError(Exception):
    pass

def error(message: str) -> NoReturn:
    raise WError(message)

class Value:
    pass

class Atom(Value, namedtuple('Atom', ['name'])):
    '''An atom.'''
    def __init__(self, name: str):
        pass

    def __repr__(self) -> str:
        return f"Atom('{self.name}')"

class Table(Value, namedtuple('Table', ['dict'])):
    '''A hash table.'''
    def __init__(self, dict_: Dict[str, Value]):
        pass

    def __repr__(self) -> str:
        return f"Table({self.dict})"

class Lambda(Value, namedtuple('Lambda', ['captures', 'parameter', 'body'])):
    '''A function (closure).'''
    def __init__(self, captures: Dict[str, Value], parameter: str, body: Table) -> None:
        pass

    def __repr__(self) -> str:
        return f"Lambda({self.captures}, {self.parameter}, {self.body})"

NULL = Atom('')
