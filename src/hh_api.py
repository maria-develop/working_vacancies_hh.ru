import json
import os
from typing import Any, List

import requests

from src.api import JobAPI
from src.vacancy import Vacancy


class HeadHunterAPI(JobAPI):
    """Выгрузка вакансий с сайта hh.ru по api"""

    def __init__(self) -> None:
        """Определение ресурса и параметров для api"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}

    def get_vacancies(self, keyword_vac: str) -> List[Any]:
        """Выгрузка вакансий с проверкой статус-кода 200"""
        self.__params["text"] = keyword_vac
        vacancies_word = []
        for page in range(1000):
            self.__params["page"] = page
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code != 200:
                break
            vacancies_word.extend(response.json().get("items", []))
        return vacancies_word

    @staticmethod
    def save_vacancies_to_json(keyword_vac: str, vacancies_word: list) -> None:
        """Сохранение вакансий в JSON файл"""
        # Определение пути к директории data в корне проекта
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
        os.makedirs(data_dir, exist_ok=True)

        # Определите имя файла с помощью ключевого слова
        filename = os.path.join(data_dir, f"vacancies.json")

        # Сохранение вакансий в JSON-файл
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(vacancies_word, f, ensure_ascii=False, indent=4)

        print(f"Вакансии по запросу '{keyword_vac}' сохранены в файл data/vacancies.json")

    @staticmethod
    def get_data_file_path(filename: str) -> str:
        """Получение абсолютного пути к файлу данных."""
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", filename)

    @staticmethod
    def load_vacancies_from_json(filename: str) -> list:
        """Загрузка вакансий из JSON файла и преобразование их в объекты Vacancy"""
        path = HeadHunterAPI.get_data_file_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            vacancies_from_json = json.load(f)
        return Vacancy.cast_to_object_list(vacancies_from_json)


# if __name__ == "__main__":
#     hh_api = HeadHunterAPI()
#     keyword = "Python"  # Ваш поисковый запрос
#     vacancies = hh_api.get_vacancies(keyword)

    # Вывод списка вакансий
    # for vacancy in vacancies:
    #     print(vacancy)

    # Сохранение вакансий в JSON-файл
    # hh_api.save_vacancies_to_json(keyword, vacancies)
