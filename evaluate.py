from model import Table, Lambda, NULL

def evaluate(environment, expression):
    '''
     - environment - Environment.
     - expression - model.Value representing code.
    '''
    assert type(expression) is Table, expression
    return expression.switch(environment.cases)

class Evaluate:
    '''
    Usage: `Evaluate(environment)(expression)`.

     - environment - dict from str to Value.
    '''
    def __init__(self, environment):
        self.cases = {
            'constant': lambda d: self.constant(d['constant']),
            'name': lambda d: self.name(d['name']),
            'lambda': lambda d: self.lambda_(d['captures'], d['parameter'], d['body']),
            'apply': lambda d: self.apply(d['function'], d['argument']),
            'table': lambda d: self.table(d['dict']),
        }
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
    a = parse('k(@foo)(@bar)', environment)
    print(evaluate(Evaluate({}), a))
