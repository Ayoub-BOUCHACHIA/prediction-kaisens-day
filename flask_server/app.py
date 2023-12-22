from flask import Flask, jsonify
from utils import read_text_from_data, predict, save, get_table, get_all_data_from_db,remove_all_data
import conf

app = Flask(__name__)


@app.route("/")
def index():
    texts = read_text_from_data()
    results_multilingual = predict(texts)
    save(results_multilingual)
    html_table = get_table(results_multilingual)
    return html_table

@app.route('/get_data')
def get_data():
    data_list = get_all_data_from_db()
    html_table = get_table(data_list,reversed=True)
    return html_table


@app.route('/clear_data')
def clear_data():
    result = remove_all_data()
    return f'Deleted {result.deleted_count} documents from MongoDB.'


if __name__ == "__main__": 
  app.run(host='0.0.0.0', port=5000)
 