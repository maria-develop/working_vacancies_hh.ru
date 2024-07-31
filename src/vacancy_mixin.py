from typing import Any, Dict, Optional


class VacancyMixin:

    _id: str
    __name: str
    area: Dict[str, Any]
    url: str
    _salary: int | Optional[Dict[str, Any]]
    description: Optional[str]
    snippet: Optional[Dict[str, Any]]
    kwargs: Any

    def __init__(self, id, name, area, url, salary, description=None, snippet=None, **kwargs) -> None:
        self._id = id
        self.__name = name
        self.area = area
        self.url = url
        self.description = description
        self._salary = salary
        self.snippet = snippet if snippet else {}
        self.kwargs = kwargs
        print(repr(self))


    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self._id}, {self.__name}, {self.area}, {self._salary}, "
            f"{self.description}, {self.snippet})"
        )
