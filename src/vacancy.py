import json
import os


class Vacancy:
    """
    Класс, представляющий вакансию.

    Атрибуты:
        name (str): Название вакансии.
        url (str): Ссылка на вакансию.
        salary (str): Зарплата, предложенная для вакансии.
        description (str): Описание вакансии.
    """

    def __init__(self, name: str, url: str, salary: str, description: str):
        if not isinstance(name, str) or not name:
            raise ValueError("Название вакансии должно быть непустой строкой")
        if not isinstance(url, str) or not url:
            raise ValueError("URL должен быть непустой строкой")
        if not isinstance(description, str):
            raise ValueError("Описание должно быть строкой")

        self.name = name
        self.url = url
        self.description = description
        self.salary = self._validate_salary(salary)

    @staticmethod
    def _validate_salary(salary: str):
        """Валидирует и преобразует значение зарплаты."""
        if salary.isdigit():
            return int(salary)
        if salary.lower() in ["не указано", "зарплата не указана"]:
            return 0
        return 0

    @staticmethod
    def cast_to_object_list(vacancies):
        """Преобразует список вакансий в список объектов класса Vacancy."""
        return [
            Vacancy(
                name=vacancy['name'],
                url=vacancy['alternate_url'],
                salary=Vacancy._get_salary_str(vacancy),
                description=vacancy.get('snippet', {}).get('responsibility', 'Не указано') if vacancy.get('snippet') and vacancy.get('snippet').get('responsibility') else 'Не указано'
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

    def __str__(self):
        """Возвращает строковое представление объекта вакансии."""
        salary_str = self.salary if self.salary != 0 else "Зарплата не указана"
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
    def load_vacancies(file_path='data/vacancies.json'):
        """Загружает вакансии из JSON файла."""
        if not os.path.exists(file_path):
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            return Vacancy.cast_to_object_list(json.load(file))

    @staticmethod
    def save_vacancies(vacancies, file_path='data/vacancies.json'):
        """Сохраняет вакансии в JSON файл."""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([vac.__dict__ for vac in vacancies], file, ensure_ascii=False, indent=4)

    @staticmethod
    def delete_vacancy(vacancy, file_path='data/vacancies.json'):
        """Удаляет вакансию из JSON файла."""
        vacancies = Vacancy.load_vacancies(file_path)
        vacancies = [v for v in vacancies if v != vacancy]
        Vacancy.save_vacancies(vacancies, file_path)


if __name__ == "__main__":
    from hh_api import HeadHunterAPI

    hh_api = HeadHunterAPI()
    keyword = "Python"
    hh_vacancies = hh_api.get_vacancies(keyword)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    for vacancy in vacancies_list:
        print(vacancy)
