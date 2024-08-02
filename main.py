import sys

from src.hh_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


def user_interaction() -> None:
    """Взаимодействие с пользователем для управления вакансиями."""
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver("vacancies.json")

    # Загружаем все вакансии из файла перед началом взаимодействия с пользователем
    vacancies = json_saver.load_vacancies()
    print(f"Загружено {len(vacancies)} вакансий из файла.")

    while True:
        print("\n1. Ввести поисковый запрос")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом в описании")
        print("4. Получить вакансии по диапазону зарплат")
        print("5. Удалить вакансию по ID")
        print("6. Добавить вакансию по ID")
        print("7. Выход")

        option = input("Введите номер пункта: ")

        if option == "1":
            keyword = input("Введите ключевое слово для поиска: ")
            hh_vacancies = hh_api.get_vacancies(keyword)
            vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
            json_saver.add_vacancies(vacancies_list)
            for vacancy in vacancies_list:
                # json_saver.add_vacancy(vacancy)
                print(vacancy)
            print(f"Добавлено {len(vacancies_list)} вакансий по запросу '{keyword}'.")
            sys.exit()

        elif option == "2":
            try:
                n = int(input("Введите количество вакансий для вывода в топ: "))
            except ValueError:
                print("Пожалуйста, введите целое число.")
                continue

            # Загрузка вакансий из hh.ru
            # hh_vacancies = hh_api.get_vacancies("")
            # vacancies = Vacancy.cast_to_object_list(hh_vacancies)
            # Загрузка вакансий из файла
            vacancies = json_saver.load_vacancies()
            if not vacancies:
                print("Нет сохраненных вакансий.")
                continue

            # Определяем функцию для извлечения зарплаты из объекта вакансии
            def get_salary(vacancy: Vacancy) -> int:
                salary = vacancy._salary
                if isinstance(salary, dict):
                    # Если salary - это словарь, извлекаем значение из поля 'from' и 'to'
                    salary_from_ = salary.get("from", 0) or 0
                    salary_to_ = salary.get("to", 0) or 0
                    return max(salary_from_, salary_to_) # Используем максимальное значение из 'from' и 'to'      if salary_from_ is not None else 0
                elif isinstance(salary, (int, float)):
                    # Если salary - это уже число
                    return salary
                return 0

            # Сортировка вакансий по убыванию зарплаты
            top_vacancies = sorted(vacancies, key=get_salary, reverse=True)[:n]
            for vacancy in top_vacancies:
                json_saver.add_vacancy(vacancy)
                print(vacancy)
            sys.exit()

        elif option == "3":
            keyword = input("Введите ключевое слово для фильтрации вакансий: ").lower()
            # Загрузка вакансий с hh.ru
            # hh_vacancies = hh_api.get_vacancies(keyword)
            # vacancies = Vacancy.cast_to_object_list(hh_vacancies)
            # Загрузка вакансий из файла
            vacancies = json_saver.load_vacancies()
            if not vacancies:
                print("Нет сохраненных вакансий.")
                continue
            filtered_vacancies = []
            for vacancy in vacancies:

                # Собираем все текстовые данные для поиска
                searchable_text = ""
                if vacancy.description:
                    searchable_text += vacancy.description.lower()
                if vacancy.snippet:
                    snippet = vacancy.snippet
                    if "requirement" in snippet and snippet["requirement"]:
                        searchable_text += " " + snippet["requirement"].lower()
                    if "responsibility" in snippet and snippet["responsibility"]:
                        searchable_text += " " + snippet["responsibility"].lower()

                # Проверяем наличие ключевого слова
                if keyword in searchable_text:
                    filtered_vacancies.append(vacancy)
            if filtered_vacancies:
                for vacancy in filtered_vacancies:
                    json_saver.add_vacancy(vacancy)  # добавила, проверить работу
                    print(vacancy)
            else:
                print(f"Вакансии с ключевым словом '{keyword}' не найдены.")
            sys.exit()

        elif option == "4":
            print("Введите диапазон зарплат")
            salary_from = int(input("от: "))
            salary_to = int(input("до: "))
            # hh_vacancies = hh_api.get_vacancies("")
            # vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
            vacancies_list = json_saver.load_vacancies()
            filtered_vacancies = [
                vacancy
                for vacancy in vacancies_list
                if isinstance(vacancy.salary, int) and salary_from <= vacancy.salary <= salary_to
            ]

            if filtered_vacancies:
                for vacancy in filtered_vacancies:
                    json_saver.add_vacancy(vacancy)   # проверить, работает ли и создается ли джейсон файл
                    print(vacancy)
            else:
                print(f"Вакансии в диапазоне зарплат от {salary_from} до {salary_to} не найдены.")
            sys.exit()

        elif option == "5":
            vacancy_id = input("Введите ID вакансии для удаления: ")
            vacancies = json_saver.load_vacancies()
            vacancy_to_delete = next((vacancy for vacancy in vacancies if vacancy.id == vacancy_id), None)
            if vacancy_to_delete:
                json_saver.delete_vacancy(vacancy_to_delete)
                print(f"Вакансия с ID {vacancy_id} удалена.")
            else:
                print(f"Вакансия с ID {vacancy_id} не найдена.")
            sys.exit()

        elif option == "6":
            vacancy_id = input("Введите ID вакансии для добавления: ")
            vacancies = json_saver.load_vacancies()
            vacancy_to_add = next((vacancy for vacancy in vacancies if vacancy.id == vacancy_id), None)
            if vacancy_to_add:
                json_saver.add_vacancy(vacancy_to_add)
                print(f"Вакансия с ID {vacancy_id} добавлена.")
            else:
                print(f"Вакансия с ID {vacancy_id} добавлена.")
            sys.exit()

        elif option == "7":
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
