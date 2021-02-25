import pandas
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def insert_author(conn, author):
    Sql_insert_author = """INSERT OR IGNORE INTO author (name) VALUES ('{}')""".format(author)
    Sql_select_author = """SELECT id FROM author WHERE name = '{}'""".format(author)
    cur = conn.cursor()
    cur.execute(Sql_insert_author)
    author = cur.execute(Sql_select_author)
    author_id = author.fetchall()
    conn.commit()
    return author_id[0][0]

def insert_agerating(conn, age_rating):
    Sql_insert_agerating = """INSERT OR IGNORE INTO age_rating (rating) VALUES ('{}')""".format(age_rating)
    Sql_select_agerating = """SELECT id FROM age_rating WHERE rating = '{}'""".format(age_rating)
    cur = conn.cursor()
    cur.execute(Sql_insert_agerating)
    agerating = cur.execute(Sql_select_agerating)
    agerating_id = agerating.fetchall()
    conn.commit()
    return agerating_id[0][0]

def insert_language(conn, language):
    Sql_insert_language = """INSERT OR IGNORE INTO language (language) VALUES ('{}')""".format(language)
    Sql_select_language = """SELECT id FROM language WHERE language = '{}'""".format(language)
    cur = conn.cursor()
    cur.execute(Sql_insert_language)
    language = cur.execute(Sql_select_language)
    language_id = language.fetchall()
    conn.commit()
    return language_id[0][0]

def insert_fanfiction(conn, title, author, age_rating, tags, characters, language, body):
    Sql_insert_fanfiction = """INSERT INTO fanfiction (title, author_id, age_rating_id, tags, characters, language_id, body) 
                                VALUES("{}", {}, {}, "{}", "{}", {}, "{}") """.format(title, author, age_rating, tags, characters, language, body)
    cur = conn.cursor()
    cur.execute(Sql_insert_fanfiction)
    conn.commit()

def main():
    database = r"fanfiction.db"
    # create connection to the database we are useing
    conn = create_connection(database)
    # Get the data that needs to be inserted into the database. Here we have a 
    # csv file that is seperated by commas. In addition, some convertions need to
    # be applied to prevent mistakes in the database and simplify accessing data. 
    data = pandas.read_csv(
        'fanfics_1.csv',
        delimiter=',',
        encoding="latin-1",
        converters={
            "title": lambda x: x.replace('"', "'"),
            "author": lambda x: x.strip("[]").replace("'", "").split(", "),
            "character": lambda x: x.replace('"', "'"),
            "additional tags": lambda x: x.replace('"', "'"),
            "body": lambda x: x.replace("\r\n", " ").replace('"', "'")})
    dataframe = pandas.DataFrame(data)

    # Every english fanfiction will be added to the database. First the author,
    # rating and language are added to their tables and the resulting ID will be
    # output so that it can be used as a forgein key in the fanfiction table.
    for index, row in dataframe.iterrows():
        if row['language'] == "English":
            print(row['work_id'])
            with conn:
                author = insert_author(conn, row["author"][0])
                age_rating = insert_agerating(conn, row["rating"])
                langauge = insert_language(conn, row["language"])
                insert_fanfiction(conn,
                    row["title"],
                    author,
                    age_rating,
                    row["additional tags"],
                    row["character"],
                    langauge,
                    row["body"])

# if the file is called the function main() will be called immediately
if __name__ == '__main__':
    main()