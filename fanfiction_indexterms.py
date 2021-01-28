import sqlite3
from sqlite3 import Error

import nltk
import math
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from lxml.etree import Element, SubElement, tostring, QName

# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


database = r"fanfiction.db"
conn = create_connection(database)
all_tokens = nltk.FreqDist()
ref_freq = nltk.FreqDist()
dictonary = {}

def get_ref_data():
    # http://www.kilgarriff.co.uk/bnc-readme.html#lemmatised
    with open("word.freq", 'r+', encoding="utf-8") as freq_data:
        for line in freq_data:
            (position, freq, word, wordtype) = line.split(" ")
            ref_freq[word] = float(freq)

def get_fanfiction(conn):
    sql_select = """SELECT fanfiction.id, fanfiction.title, author.name, age_rating.rating, 
                    fanfiction.tags, fanfiction.characters, fanfiction.language_id, fanfiction.body  
                FROM fanfiction
                INNER JOIN author ON fanfiction.author_id=author.id
                INNER JOIN age_rating ON fanfiction.age_rating_id=age_rating.id
                LIMIT 2"""
    cur = conn.cursor()
    fanfictions_execute = cur.execute(sql_select)
    fanfictions = fanfictions_execute.fetchall()
    conn.commit()
    return fanfictions


def clean_text(string):
    string = re.sub("\n", "", string)
    string = re.sub("[0-9]", " ", string)
    string = re.sub("\.\.", " ", string)
    string = re.sub("\(.*?\)", " ", string)
    string = re.sub("[\*| , |<| - |+]~_", " ", string)
    string = re.sub(" [a-z|A-Z] ", " ", string)
    string = re.sub("-", "", string)
    string = re.sub("/", " ", string)
    string = re.sub("\|", " ", string)
    string = re.sub("[a-z|A-Z]\.[a-z|A-Z]\.", " ", string)
    string = re.sub("[hH][Tt]{1,3}[pP]", " ", string)
    string = re.sub("(\.)(\S)", "\g<1> \g<2>", string)
    string = re.sub("\b[HhAaOoIiEeUuKkSs]{3,}\b", " ", string)
        
    countnew = 10
    for i in range(1, countnew):
        string = re.sub(" \. ", " ", string)
    for s in range(1, countnew):
        string = re.sub("  ", " ", string)
    
    return string

def gen_normtokens(text, characters):
    character_singletokens = []
    for character in characters:
        for char in character.split(" "):
            character_singletokens.append(char)
    lemma = WordNetLemmatizer()
    return_tokens = []
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        sentence_pos = nltk.pos_tag(nltk.word_tokenize(sentence))
        for token, pos in sentence_pos:
            if "NN" in pos and len(token) > 1:
                return_tokens.append(lemma.lemmatize(token.lower(), pos="n"))
    return_tokens = list(set(return_tokens) - set(character_singletokens))
    return return_tokens

def get_index_terms(ref_freq, tokens_freq):
    nr_tokens_ref = ref_freq.N()
    nr_tokens_documents = tokens_freq.N()
    c = float(nr_tokens_ref) / float(nr_tokens_documents)
    word_rel_freq = {lemma: math.log(c * tokens_freq.get(lemma) / ref_freq.get(lemma,1)) for lemma in tokens_freq}
    word_rel_freq = sorted(word_rel_freq.items(), key=lambda x: x[1], reverse=True)
    result_list = []
    for key, value in word_rel_freq[0:20]:
        result_list.append(key)
    return result_list
    

def fanfiction_data():
    fanfictions = get_fanfiction(conn)
    print(f'There are {len(fanfictions)} Fanfiction is the database.')
    get_ref_data()

    attr_qname = QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    xml_fanfiction_database = Element('fanfiction_database',
                                    {attr_qname: 'realschema.xsd'},
                                    nsmap={'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                            })
    xml_fanfictions = SubElement(xml_fanfiction_database, 'fanfictions')
    
    for id, title, author, age_rating, tags, characters, language, body in fanfictions:
        print("Processing Fanfiction {}/{}".format(id, len(fanfictions)), end='\r') #
        authortags = tags.split(', ')
        characters = characters.split(', ')
        text = clean_text(body)
        tokens = gen_normtokens(text, characters)
        tokens_freq = nltk.FreqDist()
        tokens_freq.update(tokens)
        index_terms = get_index_terms(ref_freq, tokens_freq)

        xml_fanfiction = SubElement(xml_fanfictions, 'fanfiction', id=str(id))
        xml_title = SubElement(xml_fanfiction, 'title').text = title
        xml_author = SubElement(xml_fanfiction, 'author').text = str(author)
        xml_age_ratings = SubElement(xml_fanfiction, 'age_rating').text = str(age_rating)
        xml_language = SubElement(xml_fanfiction, 'language').text = "English"
        xml_authortags = SubElement(xml_fanfiction, 'authortags')
        for authortag in authortags:
            xml_authortag = SubElement(xml_authortags, 'authortag').text = authortag
        xml_characters = SubElement(xml_fanfiction, 'characters')
        for character in characters:
            xml_character = SubElement(xml_characters, 'character').text = character
        xml_index_terms = SubElement(xml_fanfiction, 'index_terms')
        for index_term in index_terms:
            xml_index_term = SubElement(xml_index_terms, 'index_term').text = index_term
    
    tree = tostring(xml_fanfiction_database, xml_declaration=True, pretty_print=True, encoding="utf-8")
    file = open("fanfictions.xml", "wb")
    file.write(tree)

fanfiction_data()
