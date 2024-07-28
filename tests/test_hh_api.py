import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os

from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy


class TestHeadHunterAPI(unittest.TestCase):

    @patch("src.hh_api.requests.get")
    def test_get_vacancies(self, mock_get):
        """Тест метода get_vacancies с использованием моков"""
        # Пример ответа API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"id": "1", "name": "Vacancy 1"}, {"id": "2", "name": "Vacancy 2"}]
        }
        mock_get.return_value = mock_response

        hh_api = HeadHunterAPI()
        keyword = "Python"
        vacancies = hh_api.get_vacancies(keyword)

        # Проверка количества вакансий и их содержимого
        self.assertEqual(len(vacancies), 2000)
        self.assertEqual(vacancies[0]["name"], "Vacancy 1")
        self.assertEqual(vacancies[1]["name"], "Vacancy 2")

    def test_get_data_file_path(self):
        """Тест метода get_data_file_path"""
        hh_api = HeadHunterAPI()
        filename = "test_file.json"
        expected_path = (
            "C:\\Users\\User\\Desktop\\python_rpoject_Maria\\working_vacancies_hh.ru\\src\\..\\data\\test_file.json"
        )
        actual_path = hh_api.get_data_file_path(filename)
        self.assertEqual(expected_path, actual_path)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{"id": "1", "name": "Vacancy 1"}, {"id": "2", "name": "Vacancy 2"}]),
    )
    @patch(
        "src.hh_api.HeadHunterAPI.get_data_file_path",
        return_value=os.path.join(os.path.dirname(__file__), "..", "data", "test_file.json"),
    )
    def test_load_vacancies_from_json(self, mock_get_data_file_path, mock_file):
        """Тест метода load_vacancies_from_json с использованием моков"""
        hh_api = HeadHunterAPI()
        filename = "test_file.json"
        vacancies = hh_api.load_vacancies_from_json(filename)

        # Проверка, что файл был открыт с правильными параметрами
        expected_path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
        mock_file.assert_called_once_with(expected_path, "r", encoding="utf-8")

        # Проверка, что вакансии были корректно загружены и преобразованы в объекты Vacancy
        self.assertEqual(len(vacancies), 2)
        self.assertIsInstance(vacancies[0], Vacancy)
        self.assertEqual(vacancies[0].name, "Vacancy 1")


# if __name__ == '__main__':
#     unittest.main()
