CREATE TABLE author (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name varchar(255) UNIQUE
                                );
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE age_rating (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                rating varchar(255) UNIQUE
                                );
CREATE TABLE language (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                language varchar(255) UNIQUE
                                );
CREATE TABLE fanfiction (
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
                                );
