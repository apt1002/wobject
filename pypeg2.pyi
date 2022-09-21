from re import Pattern
from typing import NamedTuple, Literal, Any, Optional, List as ListType

class List(ListType[Any]):
    ...

class Symbol:
    check_keywords: bool

class Keyword(Symbol):
    def __init__(self, keyword: str) -> None: ...
    
K = Keyword

def attr(name: str, thing: Any = None, subtype: Any = None) -> Any: ...
def name() -> NamedTuple: ...
def csl(*thing: Any, separator: str = ",") -> Any: ...
def maybe_some(*thing: Any) -> Any: ...
def optional(*thing: Any) -> Any: ...
whitespace: Pattern[str]
def parse(
    text: str,
    thing: Any,
    filename: Optional[str] = None,
    whitespace: Pattern[str] = whitespace,
    comment: Any = None,
    keep_feeble_things: bool = False,
) -> Any: ...
