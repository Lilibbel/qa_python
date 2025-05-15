from main import BooksCollector
import pytest
# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.books_genre) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # добавление новой книги (длина 15, 0, 70 и дубликаты)
    def test_add_new_book(self,collector):
        collector.add_new_book('Маленький принц')
        assert 'Маленький принц' in collector.books_genre
        assert collector.books_genre['Маленький принц'] == ''

    def test_add_new_book_empty_name(self,collector):
        collector.add_new_book('')
        assert '' not in collector.books_genre

    def test_add_new_book_longer(self,collector):
        collector.add_new_book('Удивительное путешествие Нильса Хольгерссона с дикими гусями по Швеции')
        assert 'Удивительное путешествие Нильса Хольгерссона с дикими гусями по Швеции' not in collector.books_genre

    def test_add_new_book_duplicate(self,collector):
        collector.add_new_book('Маленький принц')
        collector.add_new_book('Маленький принц')
        assert len(collector.books_genre) == 1

    # установка жанра (валидный, книги нет в списке, жанра нет в списке)
    def test_set_book_genre(self,collector):
        collector.add_new_book('Ловец снов')
        collector.set_book_genre('Ловец снов', 'Фантастика')
        assert collector.books_genre['Ловец снов'] == 'Фантастика'

    def test_set_book_genre_not_book(self,collector):
        collector.set_book_genre('Сияние', 'Фантастика')
        assert 'Сияние' not in collector.books_genre

    def test_set_book_genre_not_genre(self,collector):
        collector.add_new_book('Тихий Дон')
        collector.set_book_genre('Тихий Дон', 'Роман-эпопея')
        assert collector.books_genre['Тихий Дон'] == ''

    # вывод жанра (существующая и несуществующая книги)
    def test_get_book_genre(self,collector):
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Фантастика')
        assert collector.get_book_genre('Оно') == 'Фантастика'

    def test_get_book_genre_nonexistent_book(self,collector):
        assert collector.get_book_genre('Война и мир') is None

    # список книг с жанром (валидные значения, нет книг, несуществующий жанр)
    def test_get_books_with_specific_genre(self,collector):
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Фантастика')
        collector.add_new_book('Ловец снов')
        collector.set_book_genre('Ловец снов', 'Фантастика')
        books_with_specific_genre = collector.get_books_with_specific_genre('Фантастика')
        assert 'Оно' in books_with_specific_genre
        assert 'Ловец снов' in books_with_specific_genre
        assert len(books_with_specific_genre) == 2

    def test_get_books_with_specific_genre_not_book(self,collector):
        assert collector.get_books_with_specific_genre('Ужасы') == []

    def test_get_books_with_specific_genre_not_genre(self,collector):
        collector.add_new_book('Одуванчики')
        assert collector.get_books_with_specific_genre('Роман') == []

    # вывод словаря с книгами и их жанрами
    def test_get_books_genre(self,collector):
        collector.add_new_book('Маленький принц')
        collector.add_new_book('Мастер и Маргарита')
        assert collector.get_books_genre() == {'Маленький принц': '', 'Мастер и Маргарита': ''}

    # книги для детей
    def test_get_books_for_children(self,collector):
        collector.add_new_book('Маленький принц')
        collector.add_new_book('Лес')
        collector.set_book_genre('Маленький принц', 'Фантастика')
        collector.set_book_genre('Лес', 'Ужасы')
        collector.add_new_book('Одуванчики')
        books_for_children = collector.get_books_for_children()
        assert 'Маленький принц' in books_for_children
        assert 'Лес' not in books_for_children
        assert 'Одуванчики' not in books_for_children

    # добавляем книгу в Избранное
    def test_add_book_in_favorites(self,collector):
        collector.add_new_book('Лес')
        collector.add_book_in_favorites('Лес')
        assert collector.favorites == ['Лес']

    def test_add_book_in_favorites_nonexistent_book(self,collector):
        collector.add_book_in_favorites('Зима')
        assert collector.favorites == []

    def test_add_book_in_favorites_duplicate(self,collector):
        collector.add_new_book('Лес')
        collector.add_book_in_favorites('Лес')
        collector.add_book_in_favorites('Лес')
        assert len(collector.favorites) == 1

    # удаляем книгу из Избранного
    def test_delete_book_from_favorites(self,collector):
        collector.add_new_book('Лес')
        collector.add_book_in_favorites('Лес')
        collector.delete_book_from_favorites('Лес')
        assert 'Лес' not in collector.favorites

    def test_delete_book_from_favorites_book_not_favorites(self,collector):
        collector.add_new_book('Лес')
        collector.delete_book_from_favorites('Лес')
        assert 'Лес' not in collector.favorites

    # получаем список Избранных книг
    def test_get_list_of_favorites_books(self,collector):
        assert collector.get_list_of_favorites_books() == []