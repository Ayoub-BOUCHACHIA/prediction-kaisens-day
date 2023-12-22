import pandas as pd
from detoxify import Detoxify
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import conf
import string
from pymongo import MongoClient
                                                           
def get_cnx_database(CONNECTION_CONF = conf.CONNECTION_CONF, DATABASE_NAME = conf.COLLECTION_NAME):
    # Create a connection using MongoClient
    cnx = MongoClient(CONNECTION_CONF)
    return cnx[DATABASE_NAME]


def remove_punctuation(text):
    # clean data remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def remove_stopwords_and_numbers(text):
    "remove numbers and stop words"
    stop_words = set(stopwords.words('french'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.lower() not in stop_words and not word.isdigit()]
    return ' '.join(filtered_text)

def get_clean_data(df):
    df['text'] = df['text'].str.lower() # lowercase character
    df['text'] = df['text'].apply(remove_stopwords_and_numbers)
    df['text'] = df['text'].apply(remove_punctuation)
    # Delete rows with missing values
    return df['text'].dropna().tolist()

def read_text_from_data():
    # read daata from json file 
    # if the file doesn't exist we should run ../scraping app
    df = pd.read_json('/data/data.json')
    data = get_clean_data(df)
    return data


def predict(list_text):
    # Predict labels from text input
    results_multilingual = Detoxify('multilingual').predict(list_text)
    results_multilingual.update({
        'text':list_text
    })
    return results_multilingual

def save(data_predicted):
    # save data after prediction 
    db = get_cnx_database()
    for i in range(len(data_predicted['text'])):
        instance = {} 
        for key in data_predicted:
             instance[key] = data_predicted[key][i]

        db[conf.COLLECTION_NAME].insert_one(instance)

def get_all_data_from_db():
    # get all data in the collection
    db = get_cnx_database()
    return list(db[conf.COLLECTION_NAME].find({}))

def remove_all_data():
    # clean all data in the collection
    db = get_cnx_database()
    return db[conf.COLLECTION_NAME].delete_many({})

def get_table(data_predicted, reversed=False):

    # build the html table for visualization
    # we have two cases:
    # either give data from the database or after pre-processing and prediction
    
    if len(data_predicted) == 0:
        return 'la base de données est vide !'
    if reversed:
        head ="""
        """
        for key in data_predicted[0]:
            head+=f"<th>{key}</th>"
        head = f"<thead><tr>{head}</tr></thead>"    
    
        rows = ""
        for instance in data_predicted:
            row = ""
            for key in instance.keys():
                rows += f"""
                    <td>{instance[key] }</td>
                """
            row = f"<tr>{row}</tr>"
            rows+=row
        rows = f"<tbody>{rows}</tbody>"
    else:
        head ="""
        """
        for key in data_predicted:
            head+=f"<th>{key}</th>"
        head = f"<thead><tr>{head}</tr></thead>"    
    
        rows = ""
        for i in range(len(data_predicted['text'])):
            row = ""
            for key in data_predicted.keys():
                rows += f"""
                    <td>{data_predicted[key][i]}</td>
                """
            row = f"<tr>{row}</tr>"
            rows+=row

        rows = f"<tbody>{rows}</tbody>"

    return f"<table>{head}{rows}</table>"