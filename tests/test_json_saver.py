import json
import os
from unittest.mock import patch, mock_open
import pytest
from src.vacancy import Vacancy
from src.json_saver import JSONSaver

@pytest.fixture
def mock_vacancy_data():
    """Создает тестовые данные вакансии."""
    return {
        'id': '123',
        'name': 'Python Developer',
        'area': {'name': 'Москва'},
        'url': 'http://example.com',
        'salary': (1000, 2000),
        'description': 'Test description',
        'snippet': {'requirement': 'Python, Django', 'responsibility': 'Developing applications'}
    }

@pytest.fixture
def mock_vacancy(mock_vacancy_data):
    """Создает объект Vacancy для тестов."""
    return Vacancy(**mock_vacancy_data)

@pytest.fixture
def json_saver():
    """Создает объект JSONSaver для тестов."""
    return JSONSaver('test_vacancies.json')

@patch('builtins.open', new_callable=mock_open)
@patch('src.json_saver.JSONSaver.get_data_file_path', return_value='test_vacancies.json')
def test_load_vacancies(mock_get_data_file_path, mock_file, json_saver, mock_vacancy_data):
    """Тест загрузки вакансий из JSON файла."""
    mock_file().read.return_value = json.dumps([mock_vacancy_data])
    vacancies = json_saver.load_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].name == 'Python Developer'

@patch('builtins.open', new_callable=mock_open)
@patch('src.json_saver.JSONSaver.get_data_file_path', return_value='test_vacancies.json')
def test_load_vacancies_file_not_found(mock_get_data_file_path, mock_file, json_saver):
    """Тест загрузки вакансий из JSON файла при отсутствии файла."""
    mock_file.side_effect = FileNotFoundError
    vacancies = json_saver.load_vacancies()
    assert vacancies == []

@patch('builtins.open', new_callable=mock_open)
@patch('src.json_saver.JSONSaver.get_data_file_path', return_value='test_vacancies.json')
def test_load_vacancies_json_decode_error(mock_get_data_file_path, mock_file, json_saver):
    """Тест загрузки вакансий из JSON файла при ошибке декодирования JSON."""
    mock_file().read.return_value = "not a json"
    vacancies = json_saver.load_vacancies()
    assert vacancies == []


if __name__ == '__main__':
    pytest.main()
