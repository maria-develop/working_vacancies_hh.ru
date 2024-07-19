import json

from src.vacancy import Vacancy


class JSONSaver:
    def __init__(self, filename='vacancies.json'):
        self.filename = filename

    def add_vacancy(self, vacancy: Vacancy):
        vacancies = self.load_vacancies()
        vacancies.append(vacancy.__dict__)
        self.save_vacancies(vacancies)

    def load_vacancies(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_vacancies(self, vacancies):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy: Vacancy):
        vacancies = self.load_vacancies()
        vacancies = [v for v in vacancies if v['url'] != vacancy.url]
        self.save_vacancies(vacancies)
