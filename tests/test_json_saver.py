import json
from unittest.mock import mock_open, patch

import pytest


@patch("builtins.open", new_callable=mock_open)
@patch("src.json_saver.JSONSaver.get_data_file_path", return_value="test_vacancies.json")
def test_load_vacancies(mock_get_data_file_path, mock_file, json_saver, mock_vacancy_data):
    """Тест загрузки вакансий из JSON файла."""
    mock_file().read.return_value = json.dumps([mock_vacancy_data])
    vacancies = json_saver.load_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].name == "Python Developer"


@patch("builtins.open", new_callable=mock_open)
@patch("src.json_saver.JSONSaver.get_data_file_path", return_value="test_vacancies.json")
def test_load_vacancies_file_not_found(mock_get_data_file_path, mock_file, json_saver):
    """Тест загрузки вакансий из JSON файла при отсутствии файла."""
    mock_file.side_effect = FileNotFoundError
    vacancies = json_saver.load_vacancies()
    assert vacancies == []


@patch("builtins.open", new_callable=mock_open)
@patch("src.json_saver.JSONSaver.get_data_file_path", return_value="test_vacancies.json")
def test_load_vacancies_json_decode_error(mock_get_data_file_path, mock_file, json_saver):
    """Тест загрузки вакансий из JSON файла при ошибке декодирования JSON."""
    mock_file().read.return_value = "not a json"
    vacancies = json_saver.load_vacancies()
    assert vacancies == []


# if __name__ == '__main__':
#     pytest.main()
