from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import sys

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Ошибка при инициализации веб-драйвера: {e}", file=sys.stderr)
        sys.exit(1)
    return driver

def search_wikipedia(driver, query):
    driver.get("https://www.wikipedia.org/")
    try:
        search_box = driver.find_element(By.NAME, "search")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)  # Дать время для загрузки страницы
    except Exception as e:
        print(f"Ошибка при выполнении поиска: {e}", file=sys.stderr)

def list_paragraphs(driver):
    try:
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
        for i, para in enumerate(paragraphs):
            print(f"{i + 1}. {para.text[:150]}...")
            input("Нажмите Enter для просмотра следующего параграфа...")
        return paragraphs
    except Exception as e:
        print(f"Ошибка при извлечении параграфов: {e}", file=sys.stderr)
        return []

def get_relevant_internal_link(driver, query):
    try:
        links = driver.find_elements(By.CSS_SELECTOR, "#bodyContent a")
        query_lower = query.lower()
        relevant_links = [link for link in links if link.get_attribute("href") and "wikipedia.org/wiki/" in link.get_attribute("href") and query_lower in link.text.lower()]
        if relevant_links:
            return random.choice(relevant_links).get_attribute("href")
        else:
            return None
    except Exception as e:
        print(f"Ошибка при извлечении внутренних ссылок: {e}", file=sys.stderr)
        return None

def main():
    driver = get_driver()
    try:
        query = input("Введите ваш запрос: ")
        search_wikipedia(driver, query)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")
            choice = input("Ваш выбор: ")

            if choice == '1':
                list_paragraphs(driver)
            elif choice == '2':
                link_href = get_relevant_internal_link(driver, query)
                if link_href:
                    try:
                        print(f"Переход по релевантной ссылке: {link_href}")
                        driver.get(link_href)
                        time.sleep(3)  # Дать время для загрузки страницы
                    except Exception as e:
                        print(f"Ошибка при переходе по ссылке: {e}", file=sys.stderr)

                    while True:
                        print("\nВыберите действие:")
                        print("1. Листать параграфы текущей статьи")
                        print("2. Перейти на одну из связанных страниц")
                        print("3. Вернуться к предыдущему меню")
                        inner_choice = input("Ваш выбор: ")

                        if inner_choice == '1':
                            list_paragraphs(driver)
                        elif inner_choice == '2':
                            link_href = get_relevant_internal_link(driver, query)
                            if link_href:
                                try:
                                    print(f"Переход по релевантной ссылке: {link_href}")
                                    driver.get(link_href)
                                    time.sleep(3)  # Дать время для загрузки страницы
                                except Exception as e:
                                    print(f"Ошибка при переходе по ссылке: {e}", file=sys.stderr)
                            else:
                                print("Нет доступных релевантных внутренних ссылок.")
                        elif inner_choice == '3':
                            break
                        else:
                            print("Неверный выбор. Попробуйте снова.")
                else:
                    print("Нет доступных релевантных внутренних ссылок.")
            elif choice == '3':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
