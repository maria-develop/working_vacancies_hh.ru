class Vacancy:
    def __init__(self, name: str, url: str, salary: str, description: str):
        self.name = name
        self.url = url
        self.salary = salary
        self.description = description

    @staticmethod
    def cast_to_object_list(vacancies):
        return [
            Vacancy(
                name=vacancy['name'],
                url=vacancy['alternate_url'],
                salary=vacancy.get('salary', {}).get('from', 'Не указано'),
                description=vacancy.get('snippet', {}).get('responsibility', 'Не указано')
            ) for vacancy in vacancies
        ]

    def __str__(self):
        return f"Вакансия: {self.name}\nСсылка: {self.url}\nЗарплата: {self.salary}\nОписание: {self.description}"

    def __eq__(self, other):
        if isinstance(other, Vacancy):
            return self.salary == other.salary
        return False

    def __lt__(self, other):
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        return False

    def __gt__(self, other):
        if isinstance(other, Vacancy):
            return self.salary > other.salary
        return False