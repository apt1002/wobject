import model, code

from typing import Dict, NamedTuple, Any
from pypeg2 import Symbol, List, K, optional, csl, attr, maybe_some, name, parse as pypeg_parse

Symbol.check_keywords = True

class Expression(List):
    grammar: Any
    def compile(self, environment: code.Environment) -> model.Table:
        '''
        Returns `model.Table`. See `code` for details.
        '''
        e: model.Table = self[0].compile(environment)
        for argument in self[1:]:
            e = code.apply(e, argument.compile(environment))
        return e

class Name:
    grammar = name()

    def compile(self, environment: code.Environment) -> model.Table:
        return environment.compile(self.get_name())

    def get_name(self) -> str:
        return self.name.name # type: ignore

class Lambda:
    grammar = K('fn'), attr('parameter', Name), '{', attr('body', Expression), '}'
    body: Expression
    parameter: Name

    def compile(self, environment: code.Environment) -> model.Table:
        parameter: str = self.parameter.get_name()
        body_environment = code.Environment(
            constant=lambda name: None if name == parameter else environment.constant(name)
        )
        body = self.body.compile(body_environment)
        captures = (
            (name, environment.compile(name))
            for name in body_environment.free_variables
            if name != parameter
        )
        return code.lambda_(captures, parameter, body)

class TableEntry:
    grammar = attr('key', Name), ':', attr('value', Expression)

class Table(List):
    grammar = '{', optional(csl(TableEntry)), '}' 

    def compile(self, environment: code.Environment) -> model.Table:
        return code.table((entry.key.name.name, entry.value.compile(environment)) for entry in self)

class Atom:
    grammar = '@', name()

    def compile(self, environment: code.Environment) -> model.Table:
        return code.atom(self.get_name())

    def get_name(self) -> str:
        return self.name.name # type: ignore

Expression.grammar = [Lambda, Table, Atom, Name], maybe_some('(', Expression, ')')

def parse(source: str, environment: Dict[str, model.Value]) -> model.Table:
    '''
     - source - str
     - environment - dict from str to Value.
    '''
    tree = pypeg_parse(source, Expression)
    env = code.Environment(constant=environment.get)
    expr: model.Table = tree.compile(env)
    for name in env.free_variables:
        model.error(f"Unknown variable {name}")
    return expr
