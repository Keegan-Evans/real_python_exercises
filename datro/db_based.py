from sqlalchemy import asc, desc, func, and_

from datro.models_1 import Book, Publisher, Author


def get_books_by_publisher(session, ascending=True):
    """Get books by publishers."""
    if not isinstance(ascending, bool):
        raise TypeError(f"ascending must be bool, not {type(ascending)}")

    direction = asc if ascending else desc

    return (
        session.query(
            Publisher.name, func.count(Book.title).label("total_books")
        )
        .join(Publisher.books)
        .group_by(Publisher.name)
        .order_by(direction("total_books"))
    )


def get_authors(session):
    """Get a list of author objects sorted by last name."""
    return session.query(Author).order_by(Author.last_name).all()


def add_new_book(session, author_name, book_title, publisher_name):
    """Add new book to system."""
    # get author first and last name
    first_name, _, last_name = author_name.partition(" ")

    book = (
        session.query(Book)
        .join(Author)
        .filter(
            and_(
                Author.first_name == first_name, Author.last_name == last_name
            )
        )
        .filter(Book.publishers.any(Publisher.name == publisher_name))
        .one_or_none()
    )

    # book by author and publisher already exists?
    if book is not None:
        return

    # book by author
    book = (
        session.query(Book)
        .join(Author)
        .filter(Book.title == book_title)
        .filter(
            and_(
                Author.first_name == first_name, Author.last_name == last_name
            )
        )
        .one_or_none()
    )

    # create new book if it doesn't exist
    if book is None:
        book = Book(title=book_title)

    # get the author
    author = session.query(Author).filter(
        and_(
            Author.first_name == first_name, Author.last_name == last_name
        ).one_or_none()
    )

    # create author if it doesn't exist
    if author is None:
        author = Author(first_name=first_name, last_name=last_name)
        session.add(author)

    # get publisher
    publisher = (
        session.query(Publisher)
        .filter(Publisher.name == publisher_name)
        .one_or_none()
    )

    # add publisher if it doesn't exist
    if publisher is None:
        publisher = Publisher(name=publisher_name)
        session.add(publisher)

    # intialize relationships
    book.author = author
    book.publishers.append(publisher)
    session.add(book)

    # commit to database
    session.commit()
