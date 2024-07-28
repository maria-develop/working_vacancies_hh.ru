from typing import Any, Dict, Optional


class VacancyMixin:

    id: str
    name: str
    area: Dict[str, Any]
    url: str
    salary: Optional[Dict[str, Any]]
    kwargs: Any


    def __init__(self, id, name, area, url, salary, description=None, snippet=None, **kwargs) -> None:
        self.id_vac = id
        self.name = name
        self.area = area
        self.url = url
        self.description = description
        self.salary = salary
        self.snippet = snippet if snippet else {}
        self.kwargs = kwargs
        print(repr(self))


    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.id}, {self.name}, {self.area}, {self.salary}, "
            f"{self.description}, {self.snippet})"
        )
