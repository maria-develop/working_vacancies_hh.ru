import unittest

from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    def test_cast_to_object_list(self):
        vacancies = [
            {
                'name': 'Python Developer',
                'alternate_url': 'http://example.com',
                'salary': {'from': 100000},
                'snippet': {'responsibility': 'Develop software'}
            }
        ]
        vacancy_objects = Vacancy.cast_to_object_list(vacancies)
        self.assertEqual(len(vacancy_objects), 1)
        self.assertEqual(vacancy_objects[0].name, 'Python Developer')
