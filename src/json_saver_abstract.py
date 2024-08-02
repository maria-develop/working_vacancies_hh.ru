from abc import ABC, abstractmethod
from typing import List
from src.vacancy import Vacancy

class JSONAbstract(ABC):
    @abstractmethod
    def save_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Сохраняет список вакансий в файл."""
        pass

    @abstractmethod
    def load_vacancies(self) -> List[Vacancy]:
        """Загружает список вакансий из файла."""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из файла."""
        pass
