import code
from pypeg2 import *

Symbol.check_keywords = True

class Expression(List):
    def compile(self, environment):
        assert isinstance(environment, code.Environment)
        '''
        Returns `model.Tuple((Atom, Value, ...))`. See `code` for details.
        '''
        e = self[0].compile(environment)
        for argument in self[1:]:
            e = code.apply(e, argument.compile(environment))
        return e

class Name:
    grammar = name()

    def compile(self, environment):
        return environment.compile(self.name.name)

class Lambda:
    grammar = K('fn'), attr('parameter', Name), '{', attr('body', Expression), '}'

    def compile(self, environment):
        parameter = self.parameter.name
        body_environment = code.Environment(
            constant=lambda name: None if name == parameter else environment.constant(name)
        )
        body = self.body.compile(body_environment)
        captures = code.table(
            (name, environment.compile(name))
            for name in body_environment.free_variables
            if name != parameter
        )
        return code.lambda_(captures, parameter, body)

class TableEntry:
    grammar = attr('key', Name), ':', attr('value', Expression)

class Table(List):
    grammar = '{', optional(csl(TableEntry)), '}' 

    def compile(self, environment):
        return code.table((entry.key.name.name, entry.value.compile(environment)) for entry in self)

class Atom:
    grammar = '@', name()

    def compile(self, environment):
        return code.atom(self.name.name)

Expression.grammar = [Lambda, Table, Atom, Name], maybe_some('(', Expression, ')')
