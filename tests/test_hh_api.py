import unittest
from unittest.mock import patch, MagicMock

from src.hh_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    @patch('requests.get')
    def test_get_vacancies(self, mock_get):
        hh_api = HeadHunterAPI()
        mock_response = MagicMock()
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response
        vacancies = hh_api.get_vacancies("Python")
        self.assertEqual(vacancies, [])
