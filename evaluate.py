'''
The interpreter. Code is represented by a Table. The key '' is the
opcode, and the remaining keys are the operands. Code is evaluated in an
environment: a dict from str to Value. The environment provides values for
captures and locals. Globals are constants compiled into the code, and not
included in the environment.

`ACTIONS` is the complete instruction set. It is a dict from opcode to function
from (environment, code) to Value, where:
 - opcode - str.
 - environment - dict from str to Value.
 - code - dict from str.
'''

from model import Table, Lambda, NULL

def evaluate_dict(environment, dict_):
    '''Map `evaluate()` over a dict.'''
    return {
        name: evaluate(environment, expression)
        for name, expression in dict_.items()
    }

def apply(function, argument):
    '''
     - function - Lambda.
     - argument - Value.
    '''
    assert type(function) is Lambda
    environment = {function.parameter: argument}
    assert function.parameter not in function.captures
    environment.update(function.captures)
    return evaluate(environment, function.body)

ACTIONS = {
    'constant': lambda _, d: d['constant'],
    'name': lambda e, d: e[d['name'].name],
    'lambda': lambda e, d: Lambda(
        evaluate_dict(e, d['captures'].dict),
        d['parameter'].name,
        d['body'],
    ),
    'apply': lambda e, d: apply(
        evaluate(e, d['function']),
        evaluate(e, d['argument']),
    ),
    'table': lambda e, d: Table(
        evaluate_dict(e, d['table'].dict),
    ),
}

def evaluate(environment, expression):
    '''
     - environment - dict from str to Value.
     - expression - model.Value representing code.
    '''
    assert type(expression) is Table, expression
    case = ACTIONS[expression.dict[''].name]
    return case(environment, expression.dict)

def built_ins():
    return {
        'null': NULL,
    }

if __name__ == '__main__':
    from parser import  parse
    environment = built_ins()
    e = parse('fn x {fn y {x}}', environment)
    environment['k'] = evaluate({}, e)
    a = parse('{a: k(@foo)(@bar)}', environment)
    print(evaluate({}, a))
