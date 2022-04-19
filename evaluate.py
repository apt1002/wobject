from model import Table, Lambda, NULL

def evaluate_dict(environment, dict_):
    '''Map `evaluate()` over a dict.'''
    return {
        name: evaluate(environment, expression)
        for name, expression in dict_.items()
    }

ACTIONS = {
    'constant': lambda _, d: d['constant'],
    'name': lambda e, d: e.environment[d['name'].name],
    'lambda': lambda e, d: Lambda(
        evaluate_dict(e, d['captures'].dict),
        d['parameter'].name,
        d['body'],
    ),
    'apply': lambda e, d: e.apply(d['function'], d['argument']),
    'table': lambda e, d: Table(evaluate_dict(e, d['table'].dict)),
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

    def apply(self, function, argument):
        function = evaluate(self, function)
        assert type(function) is Lambda
        argument = evaluate(self, argument)
        body_environment = dict(function.captures)
        body_environment[function.parameter] = argument
        return evaluate(Evaluate(body_environment), function.body)

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
