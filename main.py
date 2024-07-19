from src.hh_api import HeadHunterAPI
from src.ison_saver import JSONSaver
from src.vacancy import Vacancy


def user_interaction():
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    while True:
        print("\n1. Ввести поисковый запрос")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом в описании")
        print("4. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            keyword = input("Введите поисковый запрос: ")
            hh_vacancies = hh_api.get_vacancies(keyword)
            vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
            for vacancy in vacancies_list:
                json_saver.add_vacancy(vacancy)

        elif choice == '2':
            top_n = int(input("Введите количество вакансий для вывода в топ N: "))
            vacancies = json_saver.load_vacancies()
            vacancies_list = [Vacancy(**vacancy) for vacancy in vacancies]
            vacancies_list.sort(reverse=True)
            for vacancy in vacancies_list[:top_n]:
                print(vacancy)

        elif choice == '3':
            keyword = input("Введите ключевое слово для фильтрации вакансий: ")
            vacancies = json_saver.load_vacancies()
            filtered_vacancies = [
                Vacancy(**vacancy) for vacancy in vacancies
                if keyword.lower() in vacancy['description'].lower()
            ]
            for vacancy in filtered_vacancies:
                print(vacancy)

        elif choice == '4':
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    user_interaction()