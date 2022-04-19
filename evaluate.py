from code import Visitor
from model import Table, Lambda, NULL

class Evaluate(Visitor):
    '''
    Usage: `Evaluate(environment)(expression)`.

     - environment - dict from str to Value.
    '''
    def __init__(self, environment):
        super().__init__()
        self.environment = environment

    def constant(self, constant):
        return constant

    def name(self, name):
        return self.environment[name.name]

    def lambda_(self, captures, parameter, body):
        captures = {
            name: self(expression)
            for name, expression in captures.dict.items()
        }
        return Lambda(captures, parameter.name, body)

    def apply(self, function, argument):
        function = self(function)
        assert type(function) is Lambda
        argument = self(argument)
        body_environment = dict(function.captures)
        body_environment[function.parameter] = argument
        return Evaluate(body_environment)(function.body)

    def table(self, table):
        return Table({
            name: self(expression)
            for name, expression in table.dict.items()
        })

def built_ins():
    return {
        'null': NULL,
    }

if __name__ == '__main__':
    from parser import  parse
    environment = built_ins()
    e = parse('fn x {fn y {x}}', environment)
    environment['k'] = Evaluate({})(e)
    a = parse('k(@foo)(@bar)', environment)
    print(Evaluate({})(a))
