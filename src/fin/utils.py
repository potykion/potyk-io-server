import datetime as dt
from itertools import filterfalse
from typing import TypeVar, Iterable, Callable, Tuple, List

T = TypeVar('T')

def date_from_str(date_str):
    """
    >>> date_from_str('2022/05/22')
    datetime.date(2022, 5, 22)
    """
    return dt.datetime.strptime(date_str, '%Y/%m/%d').date()


def split_filter(iter_: Iterable[T], filter_: Callable[[T], bool]) -> Tuple[List[T], List[T]]:
    """
    >>> split_filter([1, 2, 3], lambda a: a > 1)
    ([2, 3], [1])
    """
    return list(filter(filter_, iter_)), list(filterfalse(filter_, iter_))
