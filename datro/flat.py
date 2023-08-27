import pandas as pd
from treelib import Tree

def get_data(filepath):
    """get book data from csv"""
    return pd.read_csv(filepath)

def get_books_by_publisher(data: pd.DataFrame, ascending=True):
    """Return the number of books by each"""
    return data.groupby("publisher").size().sort_values(ascending=ascending)


def add_new_book(data, author, book, publisher):
    first_name, _, last_name = author.partition(" ")
    if any(
        (data.first_name == first_name)
        & (data.last_name == last_name)
        & (data.book == book)
        & (data.publisher == publisher)
    ):
        return data

    data.loc[len(data)] = {
            "first_name": first_name,
            "last_name": last_name,
            "book": book,
            "publisher": publisher
        }
    return data

def display_books_by_publisher(books_by_publisher):
    for publisher, total_books in books_by_publisher.items():
        print(f"Publisher: {publisher}, Total Books: {total_books}")
    print()

def output_author_hierarchy(data):
    """output the data as a hierarchy list of authors"""
    authors = data.assign(
        name=data.first_name.str.cat(data.last_name, sep=" ")
    )

    authors_tree = Tree()
    
