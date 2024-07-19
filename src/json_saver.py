import json
from src.vacancy import Vacancy

class JSONSaver:
    """Класс для работы с сохранением вакансий в JSON файл."""

    def __init__(self, filename='data/vacancies.json'):
        self.filename = filename

    def save_vacancies(self, vacancies):
        """Сохраняет список вакансий в JSON файл."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([vacancy.__dict__ for vacancy in vacancies], f, ensure_ascii=False, indent=4)

    def load_vacancies(self):
        """Загружает список вакансий из JSON файла."""
        with open(self.filename, 'r', encoding='utf-8') as f:
            vacancies_data = json.load(f)
        return [Vacancy(**data) for data in vacancies_data]

    def add_vacancy(self, vacancy):
        """Добавляет вакансию в JSON файл."""
        vacancies = self.load_vacancies()
        vacancies.append(vacancy)
        self.save_vacancies(vacancies)

    def delete_vacancy(self, vacancy):
        """Удаляет вакансию из JSON файла."""
        vacancies = self.load_vacancies()
        vacancies = [v for v in vacancies if v != vacancy]
        self.save_vacancies(vacancies)
