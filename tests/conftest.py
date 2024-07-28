import os

import pytest

from src.hh_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def mock_vacancy_data():
    """Создает тестовые данные вакансии."""
    return {
        "id": "123",
        "name": "Python Developer",
        "area": {"name": "Москва"},
        "url": "http://example.com",
        "salary": (1000, 2000),
        "description": "Test description",
        "snippet": {"requirement": "Python, Django", "responsibility": "Developing applications"},
    }


# @pytest.fixture
# def mock_vacancy(mock_vacancy_data):
#     """Создает объект Vacancy для тестов."""
#     return Vacancy(**mock_vacancy_data)

# @pytest.fixture
# def json_saver():
#     """Создает объект JSONSaver для тестов."""
#     return JSONSaver('test_vacancies.json')


@pytest.fixture
def sample_vacancy():
    return Vacancy(
        id=123,
        name="Python Developer",
        area={"name": "Москва"},
        url="http://example.com",
        salary=(1000, 2000),
        description="Test description",
        snippet={"requirement": "Python, Django", "responsibility": "Developing applications"},
    )


@pytest.fixture
def json_saver():
    return JSONSaver("test_vacancies.json")

    # @pytest.fixture
    # def hh_api():
    #     return HeadHunterAPI()

    # @pytest.fixture
    # def mock_response():
    #     class MockResponse:
    #         def __init__(self, json_data, status_code):
    #             self.json_data = json_data
    #             self.status_code = status_code
    #
    #         def json(self):
    #             return self.json_data

    return MockResponse


@pytest.fixture
def vacancy_data():
    return {
        "id": 124,
        "name": "Java Developer",
        "area": {"name": "Москва"},
        "url": "http://example.com",
        "salary": (1500, 2500),
        "description": "Test description 2",
        "snippet": {"requirement": "Java, Spring", "responsibility": "Developing applications"},
    }
