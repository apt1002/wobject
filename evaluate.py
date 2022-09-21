'''
The interpreter. Code is represented by a Table. The key '' is the
opcode, and the remaining keys are the operands. Code is evaluated in an
environment: a dict from str to Value. The environment provides values for
captures and locals. Globals are constants compiled into the code, and not
included in the environment.

`ACTIONS` is the complete instruction set.
'''

from typing import Dict, Callable, cast
from model import error, Value, Atom, Table, Lambda, NULL

Environment = Dict[str, Value]

def evaluate_dict(environment: Environment, dict_: Dict[str, Table]) -> Dict[str, Value]:
    '''Map `evaluate()` over a dict.'''
    return {
        name: evaluate(environment, expression)
        for name, expression in dict_.items()
    }

def apply(function: Value, argument: Value) -> Value:
    '''
     - function - Lambda, otherwise we'll `error()`.
    '''
    if not isinstance(function, Lambda):
        error(f"{function} is not a function")
    environment = {function.parameter: argument}
    environment.update(function.captures)
    return evaluate(environment, function.body)

Code = Dict[str, Value]
Action = Callable[[Environment, Code], Value]
ACTIONS: Dict[str, Action] = {
    'constant': lambda _, d: d['constant'],
    'name': lambda e, d: e[cast(Atom, d['name']).name],
    'lambda': lambda e, d: Lambda(
        evaluate_dict(e, cast(Table, d['captures']).dict),
        cast(Atom, d['parameter']).name,
        cast(Table, d['body']),
    ),
    'apply': lambda e, d: apply(
        evaluate(e, cast(Table, d['function'])),
        evaluate(e, cast(Table, d['argument'])),
    ),
    'table': lambda e, d: Table(
        evaluate_dict(e, cast(Table, d['table']).dict),
    ),
}

def evaluate(environment: Environment, expression: Table) -> Value:
    '''
     - expression - model.Table representing code.
    '''
    case = ACTIONS[expression.dict[''].name]
    return case(environment, expression.dict)

def built_ins() -> Environment:
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
