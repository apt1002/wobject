import code
from pypeg2 import *

Symbol.check_keywords = True

class Expression:
    def compile(self, environment):
        assert isinstance(environment, code.Environment)
        '''
        Returns `model.Tuple((Atom, Value, ...))`. See `code` for details.
        '''
        return self.e.compile(environment)

class Name:
    grammar = name()

    def compile(self, environment):
        return environment.compile(self.name)

class Lambda:
    grammar = K('fn'), attr('parameter', Name), '{', attr('body', Expression), '}'

    def compile(self, environment):
        parameter = self.parameter.name
        body_environment = model.Environment(
            constant=lambda name: None if name == parameter else environment.constant(name)
        )
        body = self.body.compile(body_environment)
        captures = code.table(
            (name, environment.compile(name))
            for name in body_environment.free_variables
            if name != parameter
        )
        return code.lambda_(captures, parameter, body)

class Apply:
    grammar = attr('function', Expression), '(', attr('argument', Expression), ')'

    def compile(self, environment):
        return code.apply(self.function.compile(environment), self.argument.compile(environment))

class Atom:
    grammar = '@', name()

    def compile(self, environment):
        return code.atom(self.name.name)

class Tuple(List):
    grammar = '(', optional(csl(Expression)), ')'

    def compile(self, environment):
        return code.tuple_(e.compile(environment) for e in self)

class TableEntry:
    grammar = attr('key', Name), ':', attr('value', Expression)

class Table(List):
    grammar = '{', optional(csl(TableEntry)), '}' 

    def compile(self, environment):
        return code.table((entry.key.name.name, entry.value.compile(environment)) for entry in self)

Expression.grammar = attr('e', [Atom, Tuple, Table, Lambda, Apply, Name])
