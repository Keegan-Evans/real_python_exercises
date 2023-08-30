"""
Main functions.

Functions for running the main program for each of the sections of the relevant
 tutorial.
"""

from sys import argv
from importlib import resources
from datro.flat import (
    get_data,
    get_books_by_publisher,
    add_new_book,
    display_books_by_publisher,
    output_author_hierarchy,
)


def main(mode="flat"):
    """Run main program for model."""
    if mode == "flat":
        main_flat()
    elif mode == "database":
        main_database()
    else:
        raise ValueError(f"Unknown model: {mode}")


# flat
def main_flat():
    """Run main program for flat."""
    # have to have run "pip install -e ."
    with resources.path("datro.data", "author_book_publisher.csv") as filepath:
        data = get_data(filepath)

    books_by_publisher = get_books_by_publisher(data, ascending=False)
    display_books_by_publisher(books_by_publisher=books_by_publisher)

    # add new book
    data = add_new_book(
        data,
        author="stephen king",
        title="the stand",
        publisher="random house",
    )
    data = add_new_book(
        data, author="stephen king", title="the stand", publisher="penguin"
    )
    books_by_publisher = get_books_by_publisher(data, ascending=False)
    display_books_by_publisher(books_by_publisher=books_by_publisher)

    print(output_author_hierarchy(data=data))


# database
def main_database():
    """Run main program for database."""
    raise NotImplementedError("Database model not yet implemented.")


if __name__ == "__main__":
    main(mode=argv[1])
