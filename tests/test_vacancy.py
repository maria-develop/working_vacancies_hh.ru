import json
import unittest
from unittest.mock import mock_open, patch

import pytest

from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):

    def setUp(self):
        """Устанавливаем базовые данные для тестов"""
        self.vacancy_data = {
            "id": "123",
            "name": "Python Developer",
            "area": {"name": "Москва"},
            "alternate_url": "http://example.com",
            "salary": {"from": 1000, "to": 2000},
            "description": "Test description",
            "snippet": {"requirement": "Python, Django", "responsibility": "Developing applications"},
        }
        self.vacancy = Vacancy(
            id=self.vacancy_data["id"],
            name=self.vacancy_data["name"],
            area=self.vacancy_data["area"],
            url=self.vacancy_data["alternate_url"],
            salary=self.vacancy_data["salary"],
            description=self.vacancy_data["description"],
            snippet=self.vacancy_data["snippet"],
        )

    def test_vacancy_initialization(self):
        """Тест инициализации объекта Vacancy"""
        self.assertEqual(self.vacancy.id_vac, self.vacancy_data["id"])
        self.assertEqual(self.vacancy.name, self.vacancy_data["name"])
        self.assertEqual(self.vacancy.area, self.vacancy_data["area"])
        self.assertEqual(self.vacancy.url, self.vacancy_data["alternate_url"])
        self.assertEqual(self.vacancy.salary, (1000, 2000))
        self.assertEqual(self.vacancy.description, self.vacancy_data["description"])
        self.assertEqual(self.vacancy.snippet, self.vacancy_data["snippet"])

    def test_vacancy_str(self):
        """Тест строкового представления объекта Vacancy"""
        expected_str = (
            "Вакансия: Python Developer\n"
            "Ссылка: http://example.com\n"
            "Зарплата: 1000-2000\n"
            "Описание: Test description"
        )
        self.assertEqual(str(self.vacancy), expected_str)

    def test_vacancy_equality(self):
        """Тест сравнения вакансий по зарплате"""
        vacancy_same_salary = Vacancy(
            id="124",
            name="Another Developer",
            area={"name": "Москва"},
            url="http://another.com",
            salary={"from": 1000, "to": 2000},
            description="Another description",
            snippet={},
        )
        vacancy_diff_salary = Vacancy(
            id="125",
            name="Another Developer",
            area={"name": "Москва"},
            url="http://another.com",
            salary={"from": 1500, "to": 2500},
            description="Another description",
            snippet={},
        )
        self.assertEqual(self.vacancy, vacancy_same_salary)
        self.assertNotEqual(self.vacancy, vacancy_diff_salary)

    def test_vacancy_comparison(self):
        """Тест операторов сравнения по зарплате"""
        lower_salary = Vacancy(
            id="126",
            name="Junior Developer",
            area={"name": "Москва"},
            url="http://junior.com",
            salary={"from": 500, "to": 1000},
            description="Junior description",
            snippet={},
        )
        higher_salary = Vacancy(
            id="127",
            name="Senior Developer",
            area={"name": "Москва"},
            url="http://senior.com",
            salary={"from": 2000, "to": 3000},
            description="Senior description",
            snippet={},
        )
        self.assertGreater(self.vacancy, lower_salary)
        self.assertLess(self.vacancy, higher_salary)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_load_vacancies(self, mock_exists, mock_file):
        """Тест загрузки вакансий из JSON файла"""
        mock_file().read.return_value = json.dumps([self.vacancy_data])
        vacancies = Vacancy.load_vacancies("path/to/vacancies.json")
        self.assertEqual(len(vacancies), 1)
        self.assertIsInstance(vacancies[0], Vacancy)
        self.assertEqual(vacancies[0].name, "Python Developer")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_delete_vacancy(self, mock_exists, mock_file):
        """Тест удаления вакансии из JSON файла"""
        mock_file().read.return_value = json.dumps([self.vacancy_data])
        Vacancy.delete_vacancy(self.vacancy, "path/to/vacancies.json")
        mock_file().write.assert_called_once()
        written_data = json.loads(mock_file().write.call_args[0][0])
        self.assertEqual(len(written_data), 0)


def test_vacancy_init_valid_data():
    vacancy = Vacancy(
        id="1",
        name="Software Engineer",
        area={"name": "Moscow"},
        url="http://example.com",
        salary={"from": 1000, "to": 2000},
        description="A great job",
        snippet={"requirement": "Experience with Python", "responsibility": "Develop applications"},
    )
    assert vacancy.id_vac == "1"
    assert vacancy.name == "Software Engineer"
    assert vacancy.area == {"name": "Moscow"}
    assert vacancy.url == "http://example.com"
    assert vacancy.salary == (1000, 2000)
    assert vacancy.description == "A great job"
    assert vacancy.snippet == {"requirement": "Experience with Python", "responsibility": "Develop applications"}


def test_vacancy_init_invalid_name():
    with pytest.raises(ValueError):
        Vacancy(id="1", name="", area={"name": "Moscow"}, url="http://example.com", salary={"from": 1000, "to": 2000})


def test_vacancy_init_invalid_url():
    with pytest.raises(ValueError):
        Vacancy(id="1", name="Software Engineer", area={"name": "Moscow"}, url="", salary={"from": 1000, "to": 2000})


def test_vacancy_lt():
    vac1 = Vacancy(
        id="1",
        name="Software Engineer",
        area={"name": "Moscow"},
        url="http://example.com",
        salary={"from": 1000, "to": 2000},
    )
    vac2 = Vacancy(
        id="2",
        name="Software Engineer",
        area={"name": "Moscow"},
        url="http://example.com",
        salary={"from": 2000, "to": 3000},
    )
    assert vac1 < vac2


def test_vacancy_gt():
    vac1 = Vacancy(
        id="1",
        name="Software Engineer",
        area={"name": "Moscow"},
        url="http://example.com",
        salary={"from": 3000, "to": 4000},
    )
    vac2 = Vacancy(
        id="2",
        name="Software Engineer",
        area={"name": "Moscow"},
        url="http://example.com",
        salary={"from": 2000, "to": 3000},
    )
    assert vac1 > vac2


def test_validate_salary_dict():
    salary = {"from": 1000, "to": 2000}
    validated_salary = Vacancy._validate_salary(salary)
    assert validated_salary == (1000, 2000)


def test_validate_salary_dict_from_only():
    salary = {"from": 1000}
    validated_salary = Vacancy._validate_salary(salary)
    assert validated_salary == 1000


def test_validate_salary_dict_to_only():
    salary = {"to": 2000}
    validated_salary = Vacancy._validate_salary(salary)
    assert validated_salary == 2000


def test_validate_salary_dict_empty():
    salary = {}
    validated_salary = Vacancy._validate_salary(salary)
    assert validated_salary == 0


def test_validate_salary_str_not_specified():
    salary = "не указано"
    validated_salary = Vacancy._validate_salary(salary)
    assert validated_salary == 0


def test_validate_salary_str_digit():
    salary = "3000"
    validated_salary = Vacancy._validate_salary(salary)
    assert validated_salary == 3000


def test_validate_salary_str_range():
    salary = "1000-2000"
    validated_salary = Vacancy._validate_salary(salary)
    assert validated_salary == (1000, 2000)


def test_validate_salary_str_invalid():
    salary = "invalid"
    validated_salary = Vacancy._validate_salary(salary)
    assert validated_salary == 0


def test_get_salary_str():
    vacancy = {"salary": {"from": 1000, "to": 2000}}
    salary_str = Vacancy._get_salary_str(vacancy)
    assert salary_str == "1000-2000"


def test_get_salary_str_from_only():
    vacancy = {"salary": {"from": 1000}}
    salary_str = Vacancy._get_salary_str(vacancy)
    assert salary_str == "1000"


def test_get_salary_str_to_only():
    vacancy = {"salary": {"to": 2000}}
    salary_str = Vacancy._get_salary_str(vacancy)
    assert salary_str == "2000"


def test_get_salary_str_not_specified():
    vacancy = {"salary": None}
    salary_str = Vacancy._get_salary_str(vacancy)
    assert salary_str == "Не указано"


# if __name__ == '__main__':
#     unittest.main()
