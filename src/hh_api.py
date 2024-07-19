from abc import ABC, abstractmethod
import requests


class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str):
        pass


class HeadHunterAPI(JobAPI):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}

    def get_vacancies(self, keyword: str):
        self.params['text'] = keyword
        vacancies = []
        for page in range(20):
            self.params['page'] = page
            response = requests.get(self.url, headers=self.headers, params=self.params)
            if response.status_code != 200:
                break
            vacancies.extend(response.json().get('items', []))
        return vacancies

if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    keyword = "Python"  # Ваш поисковый запрос
    vacancies = hh_api.get_vacancies(keyword)

    # Вывод списка вакансий
    for vacancy in vacancies:
        print(vacancy)
