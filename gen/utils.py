from bs4 import BeautifulSoup, Tag
from urllib.request import urlopen
from typing import TypeVar, Callable, Any

drexel_json: dict[str, list[Any]] = { "colleges": [] }

T = TypeVar('T')
def find(filter: Callable[[T], bool], iterable: list[T]) -> T | None:
    for element in iterable:
        if filter(element): return element
    return None

def html(url: str) -> Tag:
    return BeautifulSoup(urlopen(url).read(), features = "html.parser")
