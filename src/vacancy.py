import json
import os
from typing import Any, Dict, List, Optional

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

    def __init__(self, id, name, area, url, salary, description=None, snippet=None, **kwargs) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError("Название вакансии должно быть непустой строкой")
        if not isinstance(url, str) or not url:
            raise ValueError("URL должен быть непустой строкой")

        self._id = id
        self.__name = name
        self.area = area
        self.url = url
        self.description = description
        self.snippet = snippet if snippet else {}
        self.kwargs = kwargs
        self._salary = self._validate_salary(salary)

    # def __repr__(self) -> str:
    #     return (f"Vacancy(id={self.id}, name={self.name}, area={self.area}, url={self.url}, "
    #             f"salary={self.salary}, description={self.description}, snippet={self.snippet})")

    # def __str__(self) -> str:
    #     """Возвращает строковое представление объекта вакансии."""
    #     if isinstance(self.salary, dict):
    #         salary_from = self.salary.get("from")
    #         salary_to = self.salary.get("to")
    #         currency = self.salary.get('currency', 'RUR')
    #         if salary_from and salary_to:
    #             salary_str = f"от {salary_from} до {salary_to} {currency}"
    #         elif salary_from:
    #             salary_str = f"от {salary_from} {currency}"
    #         elif salary_to:
    #             salary_str = f"до {salary_to} {currency}"
    #         else:
    #             salary_str = "Зарплата не указана"
    #     elif isinstance(self.salary, (int, float, str)):
    #         return f"{self.salary}"
    #     else:
    #         salary_str = str(self.salary) if self.salary else "Зарплата не указана"
    #
    #     return (f"Вакансия: {self.name}"
    #             f"\nСсылка: {self.url}\nЗарплата: {salary_str}\nОписание: {self.snippet['responsibility']}")

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self.__name

    @property
    def salary(self):
        return self._salary

    def __str__(self) -> str:
        """Возвращает строковое представление объекта вакансии."""
        if isinstance(self._salary, dict):
            salary_str = (
                f"{self._salary[0]}-{self._salary[1]}"
                if isinstance(self._salary, tuple)
                else (self._salary if self._salary != 0 else "Зарплата не указана")
            )
        elif isinstance(self._salary, (int, float, str)):
            salary_str = f"{self._salary}"
        else:
            salary_str = str(self._salary) if self._salary else "Зарплата не указана"
        return (f"Вакансия: "
            f"{self.__name}\nСсылка: {self.url}\nЗарплата: {salary_str}\nОписание: {self.snippet.get('responsibility', "Нет информации")}")

    def __eq__(self, other: int) -> Any:
        """Сравнивает зарплату текущей вакансии с другой вакансией на равенство."""
        if isinstance(other, Vacancy):
            return self._salary == other._salary
        return False

    def __lt__(self, other: int) -> Any:
        """Сравнивает зарплату текущей вакансии с другой вакансией на меньше."""
        if isinstance(other, Vacancy):
            return self._salary < other._salary
        return False

    def __gt__(self, other: int) -> Any:
        """Сравнивает зарплату текущей вакансии с другой вакансией на больше"""
        if isinstance(other, Vacancy):
            return self._salary > other._salary
        return False

    @staticmethod
    def _validate_salary(salary: (int, float, list, tuple)) -> int | tuple[int, int] | None:
        """Валидирует и преобразует значение зарплаты."""
        if isinstance(salary, dict):
            from_salary = salary.get("from")
            to_salary = salary.get("to")
            if from_salary and to_salary:
                return from_salary, to_salary
            if from_salary:
                return from_salary
            if to_salary:
                return to_salary
            return 0
        elif isinstance(salary, (int, float)):
            # if salary.lower() in ["не указано", "зарплата не указана", ""]:
            #     return 0
            return salary
            # if salary.isdigit():
            #     return int(salary)
            # salary_parts = salary.replace(" ", "").split("-")
            # if len(salary_parts) == 2 and all(part.isdigit() for part in salary_parts):
            #     try:
            #         return int(salary_parts[0]), int(salary_parts[1])
            #     except ValueError:
            #         return 0
            # try:
            #     return int(salary_parts[0])
            # except ValueError:
            #     return 0
        return 0

    def _get_salary_str(self) -> str:
        """Возвращает зарплату в виде строки."""
        if isinstance(self._salary, tuple):
            return f"{self._salary[0]}-{self._salary[1]}"
        if isinstance(self._salary, int):
            return f"{self._salary}"
        return "Зарплата не указана"

    @classmethod
    def cast_to_object_list(cls, vacancies: List[Dict[str, Any]]) -> list:
        """Преобразует список вакансий в список объектов класса Vacancy."""
        return [
            cls(
                id=vacancy.get("id", "Не указано"),
                name=vacancy.get("name", "Не указано"),
                area=vacancy.get("area", {}),
                url=vacancy.get("alternate_url", "Не указано"),
                salary=vacancy.get("salary", 0),
                description=vacancy.get("description", "Не указано"),
                snippet=vacancy.get("snippet", {}),
            )
            for vacancy in vacancies
        ]

    # @staticmethod
    # def _get_salary_str(vacancy: Dict[str, Any]) -> str:
    #     """Возвращает зарплату в виде строки."""
    #     salary = vacancy.get("salary")
    #     if salary:
    #         from_salary = salary.get("from")
    #         to_salary = salary.get("to")
    #         if from_salary and to_salary:
    #             return f"{from_salary}-{to_salary}"
    #         if from_salary:
    #             return str(from_salary)
    #         if to_salary:
    #             return str(to_salary)
    #     return "Не указано"

    def to_dict(self) -> Dict[str, Any]:
        """Возвращает словарное представление объекта вакансии."""
        return {
            "id": self._id,
            "name": self.__name,
            "area": self.area,
            "url": self.url,
            "salary": self._salary,
            "description": self.description,
            "snippet": self.snippet,
            **self.kwargs,
        }


# if __name__ == "__main__":
#     from hh_api import HeadHunterAPI
#
#     hh_api = HeadHunterAPI()
#     keyword = "экономист"
#     hh_vacancies = hh_api.get_vacancies(keyword)
# vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

# for vacancy in vacancies_list:
#     print(vacancy)
