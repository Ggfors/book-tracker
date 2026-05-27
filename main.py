import json
import os
from datetime import datetime

DATA_FILE = "books.json"

def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []

def save_books(books):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

def add_book():
    books = load_books()
    print("\n--- Добавление книги ---")
    author = input("Автор: ").strip()
    title = input("Название: ").strip()
    for book in books:
        if book["author"].lower() == author.lower() and book["title"].lower() == title.lower():
            print("Такая книга уже есть в списке.")
            return
    while True:
        try:
            rating = int(input("Оценка (1-5): ").strip())
            if 1 <= rating <= 5:
                break
            else:
                print("Оценка должна быть от 1 до 5.")
        except ValueError:
            print("Введите целое число.")
    date_str = input("Дата прочтения (ГГГГ-ММ-ДД): ").strip()
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Неверный формат даты. Будет установлена сегодняшняя дата.")
        date_str = datetime.today().strftime("%Y-%m-%d")
    book = {
        "author": author,
        "title": title,
        "rating": rating,
        "date_read": date_str
    }
    books.append(book)
    save_books(books)
    print(f"Книга '{title}' добавлена.")

def show_all_books():
    books = load_books()
    print("\n--- Все книги ---")
    if not books:
        print("Список пуст.")
        return
    for i, book in enumerate(books, 1):
        print(f"{i}. {book['author']} - {book['title']} | Оценка: {book['rating']} | Дата: {book['date_read']}")

def show_average_rating():
    books = load_books()
    if not books:
        print("Список книг пуст.")
        return
    avg = sum(book['rating'] for book in books) / len(books)
    print(f"\nСредняя оценка: {avg:.2f}")

def show_author_stats():
    books = load_books()
    if not books:
        print("Список книг пуст.")
        return
    stats = {}
    for book in books:
        author = book['author']
        stats[author] = stats.get(author, 0) + 1
    print("\n--- Статистика по авторам ---")
    for author, count in sorted(stats.items()):
        print(f"{author}: {count} книг(а)")

def delete_book():
    books = load_books()
    if not books:
        print("Список книг пуст.")
        return
    show_all_books()
    try:
        idx = int(input("\nВведите номер книги для удаления (0 - отмена): ").strip())
        if idx == 0:
            return
        if 1 <= idx <= len(books):
            removed = books.pop(idx - 1)
            save_books(books)
            print(f"Книга '{removed['title']}' удалена.")
        else:
            print("Неверный номер.")
    except ValueError:
        print("Введите число.")

def main():
    while True:
        print("\n" + "=" * 30)
        print("ТРЕКЕР ПРОЧИТАННЫХ КНИГ")
        print("=" * 30)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        print("=" * 30)
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            show_average_rating()
        elif choice == "4":
            show_author_stats()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()