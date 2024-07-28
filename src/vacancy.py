import json
import os
from typing import Union, Tuple, Optional

from src.vacancy_mixin import VacancyMixin


class Vacancy(VacancyMixin):
    """
    Класс, представляющий вакансию.

    Атрибуты:
        id (str): ID вакансии.
        name (str): Название вакансии.
        area (dict): Регион вакансии.
        url (str): Ссылка на вакансию.
        salary (Union[int, Tuple[int, int]]): Зарплата, предложенная для вакансии.
        description (Optional[str]): Описание вакансии.
        snippet (dict): Краткая информация о вакансии.
    """

    def __init__(self, id: str, name: str, area: dict, url: str, salary: Union[int, Tuple[int, int]],
                 description: Optional[str] = None, snippet: dict = None, **kwargs) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError("Название вакансии должно быть непустой строкой")
        if not isinstance(url, str) or not url:
            raise ValueError("URL должен быть непустой строкой")

        self.id_vac = id
        self.name = name
        self.area = area
        self.url = url
        self.description = description
        self.salary = self._validate_salary(salary)
        self.snippet = snippet if snippet else {}
        self.kwargs = kwargs

    # def __repr__(self) -> str:
    #     return (f"Vacancy(id={self.id_vac}, name={self.name}, area={self.area}, url={self.url}, "
    #             f"salary={self.salary}, description={self.description}, snippet={self.snippet})")

    def __str__(self):
        """Возвращает строковое представление объекта вакансии."""
        salary_str = f"{self.salary[0]}-{self.salary[1]}" if isinstance(self.salary, tuple) else (
            self.salary if self.salary != 0 else "Зарплата не указана")
        return f"Вакансия: {self.name}\nСсылка: {self.url}\nЗарплата: {salary_str}\nОписание: {self.description}"

    def __eq__(self, other):
        """Сравнивает зарплату текущей вакансии с другой вакансией на равенство."""
        if isinstance(other, Vacancy):
            return self.salary == other.salary
        return False

    def __lt__(self, other):
        """Сравнивает зарплату текущей вакансии с другой вакансией на меньше."""
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        return False

    def __gt__(self, other):
        """Сравнивает зарплату текущей вакансии с другой вакансией на больше"""
        if isinstance(other, Vacancy):
            return self.salary > other.salary
        return False

    @staticmethod
    def _validate_salary(salary):
        """Валидирует и преобразует значение зарплаты."""
        if isinstance(salary, dict):
            from_salary = salary.get('from')
            to_salary = salary.get('to')
            if from_salary and to_salary:
                return from_salary, to_salary
            if from_salary:
                return from_salary
            if to_salary:
                return to_salary
            return 0
        elif isinstance(salary, str):
            if salary.lower() in ["не указано", "зарплата не указана", ""]:
                return 0
            if salary.isdigit():
                return int(salary)
            salary_parts = salary.replace(' ', '').split('-')
            if len(salary_parts) == 2 and all(part.isdigit() for part in salary_parts):
                try:
                    return int(salary_parts[0]), int(salary_parts[1])
                except ValueError:
                    return 0
            try:
                return int(salary_parts[0])
            except ValueError:
                return 0
        return 0

    @staticmethod
    def cast_to_object_list(vacancies):
        """Преобразует список вакансий в список объектов класса Vacancy."""
        return [
            Vacancy(
                id=vacancy.get('id', 'Не указано'),
                name=vacancy.get('name', 'Не указано'),
                area=vacancy.get('area', {}),
                url=vacancy.get('alternate_url', 'Не указано'),
                salary=vacancy.get('salary', {}),
                description=vacancy.get('description', 'Не указано'),
                snippet=vacancy.get('snippet', {})
            ) for vacancy in vacancies
        ]

    @staticmethod
    def _get_salary_str(vacancy):
        """Возвращает зарплату в виде строки."""
        salary = vacancy.get('salary')
        if salary:
            from_salary = salary.get('from')
            to_salary = salary.get('to')
            if from_salary and to_salary:
                return f"{from_salary}-{to_salary}"
            if from_salary:
                return str(from_salary)
            if to_salary:
                return str(to_salary)
        return "Не указано"

    @staticmethod
    def load_vacancies(file_p='C:/Users/User/Desktop/python_rpoject_Maria/working_vacancies_hh.ru/data/vacancies.json'):
        """Загружает вакансии из JSON файла."""
        if not os.path.exists(file_p):
            return []

        with open(file_p, 'r', encoding='utf-8') as file:
            return Vacancy.cast_to_object_list(json.load(file))

    @staticmethod
    def save_vacancies(vacancies,
                       file_p='C:/Users/User/Desktop/python_rpoject_Maria/working_vacancies_hh.ru/data/vacancies.json'):
        """Сохраняет вакансии в JSON файл."""
        with open(file_p, 'w', encoding='utf-8') as file:
            json.dump([vac.__dict__ for vac in vacancies], file, ensure_ascii=False, indent=4)

    @staticmethod
    def delete_vacancy(vacancy,
                       file_p='C:/Users/User/Desktop/python_rpoject_Maria/working_vacancies_hh.ru/data/vacancies.json'):
        """Удаляет вакансию из JSON файла."""
        vacancies = Vacancy.load_vacancies(file_p)
        vacancies = [v for v in vacancies if v != vacancy]
        Vacancy.save_vacancies(vacancies, file_p)

    def to_dict(self):
        pass


# if __name__ == "__main__":
#     from hh_api import HeadHunterAPI
#
#     hh_api = HeadHunterAPI()
#     keyword = "экономист"
#     hh_vacancies = hh_api.get_vacancies(keyword)
    # vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    # for vacancy in vacancies_list:
    #     print(vacancy)
