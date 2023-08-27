from importlib import resources
from datro.flat import (
    get_data, get_books_by_publisher, add_new_book, display_books_by_publisher,
    output_author_hierarchy
)
def main():
    with resources.path(
        "datro.data", "author_book_publisher.csv"
    ) as filepath:
        data = get_data(filepath)

    books_by_publisher = get_books_by_publisher(data, ascending=False)
    display_books_by_publisher(books_by_publisher=books_by_publisher)

    # add new book
    data = add_new_book(
        data,
        author="stephen_king",
        book="the stand",
        publisher="random house"
    )
    books_by_publisher = get_books_by_publisher(data, ascending=False)
    display_books_by_publisher(books_by_publisher=books_by_publisher)

    print(output_author_hierarchy(data=data))
    



if __name__ == '__main__':
    main()    