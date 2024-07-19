import json
import os
from abc import ABC, abstractmethod
import requests

from src.vacancy import Vacancy


class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str):
        pass


class HeadHunterAPI(JobAPI):
    """Выгрузка вакансий с сайта hh.ru по api"""
    def __init__(self):
        """Определение ресурса и параметров для api"""
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}

    def get_vacancies(self, keyword: str):
        """Выгрузка вакансий с проверкой статус-кода 200"""
        self.params['text'] = keyword
        vacancies = []
        for page in range(20):
            self.params['page'] = page
            response = requests.get(self.url, headers=self.headers, params=self.params)
            if response.status_code != 200:
                break
            vacancies.extend(response.json().get('items', []))
        return vacancies


    def save_vacancies_to_json(self, keyword: str, vacancies: list):
        """Сохранение вакансий в JSON файл"""
        # Определение пути к директории data в корне проекта
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        # os.makedirs('C:/Users/User/Desktop/python_rpoject_Maria/working_vacancies_hh.ru/data', exist_ok=True)

        # Определите имя файла с помощью ключевого слова
        filename = os.path.join(data_dir, f"{keyword}_vacancies.json")
        # filename = os.path.join("C:/Users/User/Desktop/python_rpoject_Maria/working_vacancies_hh.ru/data", f"{keyword}_vacancies.json")

        # Сохранение вакансий в JSON-файл
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)

        print(f"Вакансии сохранены в файл {filename}")

    @staticmethod
    def get_data_file_path(filename: str) -> str:
        """Получение абсолютного пути к файлу данных."""
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', filename)

    @staticmethod
    def load_vacancies_from_json(filename: str) -> list:
        """Загрузка вакансий из JSON файла и преобразование их в объекты Vacancy"""
        path = HeadHunterAPI.get_data_file_path(filename)
        with open(path, 'r', encoding='utf-8') as f:
            vacancies = json.load(f)
        return Vacancy.cast_to_object_list(vacancies)


if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    keyword = "Python"  # Ваш поисковый запрос
    vacancies = hh_api.get_vacancies(keyword)

    # Вывод списка вакансий
    # for vacancy in vacancies:
    #     print(vacancy)

    # Сохранение вакансий в JSON-файл
    hh_api.save_vacancies_to_json(keyword, vacancies)
