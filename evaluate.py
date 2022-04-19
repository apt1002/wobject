from model import Table, Lambda, NULL

ACTIONS = {
    'constant': lambda e, d: e.constant(d['constant']),
    'name': lambda e, d: e.name(d['name']),
    'lambda': lambda e, d: e.lambda_(d['captures'], d['parameter'], d['body']),
    'apply': lambda e, d: e.apply(d['function'], d['argument']),
    'table': lambda e, d: e.table(d['table']),
}

def evaluate(environment, expression):
    '''
     - environment - Environment.
     - expression - model.Value representing code.
    '''
    assert type(expression) is Table, expression
    case = ACTIONS[expression.dict[''].name]
    return case(environment, expression.dict)

class Evaluate:
    '''
    Usage: `Evaluate(environment)(expression)`.

     - environment - dict from str to Value.
    '''
    def __init__(self, environment):
        self.environment = environment

    def constant(self, constant):
        return constant

    def name(self, name):
        return self.environment[name.name]

    def lambda_(self, captures, parameter, body):
        captures = {
            name: evaluate(self, expression)
            for name, expression in captures.dict.items()
        }
        return Lambda(captures, parameter.name, body)

    def apply(self, function, argument):
        function = evaluate(self, function)
        assert type(function) is Lambda
        argument = evaluate(self, argument)
        body_environment = dict(function.captures)
        body_environment[function.parameter] = argument
        return evaluate(Evaluate(body_environment), function.body)

    def table(self, table):
        return Table({
            name: evaluate(self, expression)
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
    environment['k'] = evaluate(Evaluate({}), e)
    a = parse('{a: k(@foo)(@bar)}', environment)
    print(evaluate(Evaluate({}), a))
