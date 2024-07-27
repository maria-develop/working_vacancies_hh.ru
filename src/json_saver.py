import json
import os

from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy

class JSONSaver:
    """Класс для работы с сохранением вакансий в JSON файл."""

    def __init__(self, filename):
        self.filename = self.get_data_file_path(filename)

    @staticmethod
    def get_data_file_path(filename: str) -> str:
        """Получение абсолютного пути к файлу данных."""
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', filename)

    # @staticmethod
    # def load_vacancies_from_json(filename: str) -> list:
    #     """Загрузка вакансий из JSON файла и преобразование их в объекты Vacancy"""
    #     path = HeadHunterAPI.get_data_file_path(filename)
    #     with open(path, 'r', encoding='utf-8') as f:
    #         vacancies = json.load(f)
    #     return Vacancy.cast_to_object_list(vacancies)

    def save_vacancies(self, vacancies):
        """Сохраняет список вакансий в JSON файл."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([vacancy.__dict__ for vacancy in vacancies], f, ensure_ascii=False, indent=4)


    def load_vacancies(self):
        """Загружает список вакансий из JSON файла."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                vacancies_data = json.load(f)
            # print(f"Загружено {len(vacancies_data)} вакансий из файла.")
            return [Vacancy(**data) for data in vacancies_data]
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден.")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON в файле {self.filename}.")
            return []
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return []


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
