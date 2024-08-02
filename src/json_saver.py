import json
import os
from typing import Any, List

from src.json_saver_abstract import JSONAbstract
from src.vacancy import Vacancy


class JSONSaver(JSONAbstract):
    """Класс для работы с сохранением вакансий в JSON файл."""

    def __init__(self, filename: str) -> None:
        self.filename = self.get_data_file_path(filename)

    @staticmethod
    def get_data_file_path(filename: str) -> str:
        """Получение абсолютного пути к файлу данных."""
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", filename)

    def save_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Сохраняет список вакансий в JSON файл."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([vacancy.to_dict() for vacancy in vacancies], f, ensure_ascii=False, indent=4)

    def load_vacancies(self) -> List[Vacancy]:
        """Загружает список вакансий из JSON файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                vacancies_data = json.load(f)
            # print(f"Загружено {len(vacancies_data)} вакансий из файла.")
            return [Vacancy(**data) for data in vacancies_data]
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден.")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON в файле vacancies.json.")
            return []
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return []

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в JSON файл."""
        vacancies = self.load_vacancies()
        vacancies.append(vacancy)
        self.save_vacancies(vacancies)

    def add_vacancies(self, vacancies: list[Vacancy]) -> None:
        """Добавляет все 2000 вакансий"""
        old_vacancies = self.load_vacancies()
        old_vacancies.extend(vacancies)
        self.save_vacancies(old_vacancies)

    def delete_vacancy(self, vacancy: Vacancy) -> Any:
        """Удаляет вакансию из JSON файла."""
        vacancies = self.load_vacancies()
        vacancies = [v for v in vacancies if v._id != vacancy._id]
        self.save_vacancies(vacancies)
