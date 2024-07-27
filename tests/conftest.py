import pytest
from unittest.mock import MagicMock
from src.hh_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def mock_hh_api():
    api = MagicMock(spec=HeadHunterAPI)
    api.get_vacancies.return_value = [
        {'id': '1', 'name': 'Python Developer', 'area': {'name': 'Москва'},
         'url': 'http://example.com', 'salary': {'from': 1000}, 'description': 'Test description',
         'snippet': {'requirement': 'Python', 'responsibility': 'Developing applications'}},
        {'id': '2', 'name': 'Java Developer', 'area': {'name': 'Санкт-Петербург'},
         'url': 'http://example.com', 'salary': {'from': 2000}, 'description': 'Another description',
         'snippet': {'requirement': 'Java', 'responsibility': 'Developing Java applications'}}
    ]
    return api


@pytest.fixture
def mock_json_saver():
    saver = MagicMock(spec=JSONSaver)
    saver.load_vacancies.return_value = [
        Vacancy(id=1, name='Python Developer', area={'name': 'Москва'}, url='http://example.com',
                salary=1000, description='Test description',
                snippet={'requirement': 'Python', 'responsibility': 'Developing applications'}),
        Vacancy(id=2, name='Java Developer', area={'name': 'Санкт-Петербург'}, url='http://example.com',
                salary=2000, description='Another description',
                snippet={'requirement': 'Java', 'responsibility': 'Developing Java applications'})
    ]
    return saver


@pytest.fixture
def mock_vacancy():
    return Vacancy(id=123, name='Python Developer', area={'name': 'Москва'},
                   url='http://example.com', salary=0, description='Test description',
                   snippet={'requirement': 'Python, Django', 'responsibility': 'Developing applications'})
