import pytest
from src.vacancy_mixin import VacancyMixin
from unittest.mock import MagicMock

class TestVacancy(VacancyMixin):
    def __init__(self, id, name, area, url, salary, description, snippet):
        self.id = id
        self.name = name
        self.area = area
        self.url = url
        self.salary = salary
        self.description = description
        self.snippet = snippet
        super().__init__()

def test_vacancy_mixin_repr():
    vacancy = TestVacancy(
        id="1",
        name="Software Engineer",
        area={"name": "Moscow"},
        url="http://example.com",
        salary={"from": 1000, "to": 2000},
        description="A great job",
        snippet={"requirement": "Experience with Python", "responsibility": "Develop applications"}
    )
    expected_repr = ("TestVacancy(1, Software Engineer, {'name': 'Moscow'}, {'name': 'Moscow'}, "
                     "{'from': 1000, 'to': 2000}, A great job, "
                     "{'requirement': 'Experience with Python', 'responsibility': 'Develop applications'})")
    assert repr(vacancy) == expected_repr

def test_vacancy_mixin_init_prints_repr(capfd):
    vacancy = TestVacancy(
        id="1",
        name="Software Engineer",
        area={"name": "Moscow"},
        url="http://example.com",
        salary={"from": 1000, "to": 2000},
        description="A great job",
        snippet={"requirement": "Experience with Python", "responsibility": "Develop applications"}
    )
    expected_repr = ("TestVacancy(1, Software Engineer, {'name': 'Moscow'}, {'name': 'Moscow'}, "
                     "{'from': 1000, 'to': 2000}, A great job, "
                     "{'requirement': 'Experience with Python', 'responsibility': 'Develop applications'})\n")
    captured = capfd.readouterr()
    assert captured.out == expected_repr