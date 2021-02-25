import sqlite3
from sqlite3 import Error


def create_connection(db_file):
        conn = None
        try:
                conn = sqlite3.connect(db_file)
        except Error as e:
                print(e)
        return conn

def create_table(conn, create_table_sql):
        try:
                c = conn.cursor()
                c.execute(create_table_sql)
        except Error as e:
                print(e)

def main():
        database = r"fanfiction.db"
        sql_create_tables_author = """CREATE TABLE IF NOT EXISTS author (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name varchar(255) UNIQUE
                                );"""
        sql_create_tables_agerating = """CREATE TABLE IF NOT EXISTS age_rating (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                rating varchar(255) UNIQUE
                                );"""
        sql_create_tables_language = """CREATE TABLE IF NOT EXISTS language (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                language varchar(255) UNIQUE
                                );"""
        sql_create_tables_fanfiction = """CREATE TABLE IF NOT EXISTS fanfiction (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title varchar(255),
                                author_id INTEGER,
                                age_rating_id INTEGER,
                                tags varchar(255),
                                characters varchar(255),
                                language_id INTEGER,
                                body text,
                                FOREIGN KEY (author_id) REFERENCES author (id),
                                FOREIGN KEY (age_rating_id) REFERENCES age_rating (id),
                                FOREIGN KEY (language_id) REFERENCES language (id)
                                ); """

        # Create Connection to the database that we are using.                  
        conn = create_connection(database)

        # Create every table in the database. First the tables that will be
        # referenced in the main table need to be created.
        if conn is not None:
                create_table(conn, sql_create_tables_author)
                create_table(conn, sql_create_tables_agerating)
                create_table(conn, sql_create_tables_language)
                create_table(conn, sql_create_tables_fanfiction)
        else:
                print("Error cannot crate the database connection.")

# if the file is called the function main() will be called immediately
if __name__ == '__main__':
        main()
        