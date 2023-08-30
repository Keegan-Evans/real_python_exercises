"""Flat section helper functions."""
import pandas as pd
from treelib import Tree


def get_data(filepath):
    """Get book data from csv."""
    return pd.read_csv(filepath)


def get_books_by_publisher(data: pd.DataFrame, ascending=True):
    """Return the number of books by each."""
    return data.groupby("publisher").size().sort_values(ascending=ascending)


def add_new_book(data, author, title, publisher):
    """Add a new book to the data."""
    first_name, _, last_name = author.partition(" ")
    print(first_name, last_name)
    if any(
        (data.first_name == first_name)
        & (data.last_name == last_name)
        & (data.title == title)
        & (data.publisher == publisher)
    ):
        return data

    # refactored from original to be compatible with pandas>2.0
    # dataframes no longer have an append method
    # the justification makes sense(keeps new users from trying to use it
    # like the standard python `list.append`, which does modify in place while
    # the `DataFrame.append` method did not. This was not a big deal if used
    # to functional programming approaches)
    data.loc[len(data)] = {
        "first_name": first_name,
        "last_name": last_name,
        "title": title,
        "publisher": publisher,
    }
    return data


def display_books_by_publisher(books_by_publisher):
    """Display the number of books by publisher."""
    for publisher, total_books in books_by_publisher.items():
        print(f"Publisher: {publisher}, Total Books: {total_books}")
    print()


def output_author_hierarchy(data):
    """Output the data as a hierarchy list of authors."""
    authors = data.assign(
        name=data.first_name.str.cat(data.last_name, sep=" ")
    )
    print(authors)

    authors_tree = Tree()

    authors_tree.create_node("Authors", "authors")

    for author, books in authors.groupby("name"):
        authors_tree.create_node(author, author, parent="authors")
        for title, publishers in books.groupby("title")["publisher"]:
            book_id = f"{author}:{title}"
            authors_tree.create_node(title, book_id, parent=author)
            for publisher in publishers:
                authors_tree.create_node(publisher, parent=book_id)

    # Output the heirarchichal authors data
    authors_tree.show()
