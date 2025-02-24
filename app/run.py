
# imports

from collections import Counter
import json, plotly
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from flask import Flask
from flask import render_template, request, jsonify
import numpy as np
import operator
from plotly.graph_objs import Bar
from pprint import pprint
import re
from sklearn.externals import joblib
from sqlalchemy import create_engine

# initializing Flask app
app = Flask(__name__)

def tokenize(text):
    """
    clean text removing punctuations

    Args:
    text str: Messages as text data

    Returns:
    words list: Processed text after tokenizing and lemmatizing
    """
    # Normalize text
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    
    # tokenize text
    words = word_tokenize(text)
    
    # remove stop words
    stopwords_ = stopwords.words("english")
    removed_stop = [word for word in words if word not in stopwords_]
    
    
    lemmatizer = WordNetLemmatizer()
    words =  [lemmatizer.lemmatize(word, pos='v') for word in words]
    return words


# load data
engine = create_engine('sqlite:///data/DisasterResponse.db')
df = pd.read_sql_table('DisasterResponse', engine)

# load model
model = joblib.load("models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    """
    Process the data to create visualizations and render a web page with the plots.

    Args:
    df (DataFrame): DataFrame containing the cleaned messages and categories data.

    Returns:
    str: Rendered HTML template with plotly figures.

    """
    
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    category_proportions = df[df.columns[4:]].sum() / len(df)
    category_proportions = category_proportions.sort_values(ascending=False)
    category_names = list(category_proportions.index)
    
    words_with_repetition = []
    for text in df['message'].values:
        tokenized_words = tokenize(text)
        words_with_repetition.extend(tokenized_words)
    
    word_count_dict = Counter(words_with_repetition)
    sorted_word_count_dict = dict(sorted(word_count_dict.items(), key=operator.itemgetter(1), reverse=True))
    
    top_10_words = dict(list(sorted_word_count_dict.items())[:10])
    words = list(top_10_words.keys())
    count_proportions = 100 * np.array(list(top_10_words.values())) / df.shape[0]
    
    print(words)
    
    # Create visuals
    figures = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],
            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {'title': "Count"},
                'xaxis': {'title': "Genre"}
            }
        },
        {
            'data': [
                Bar(
                    x=category_names,
                    y=category_proportions
                )
            ],
            'layout': {
                'title': 'Proportion of Messages <br> by Category',
                'yaxis': {'title': "Proportion", 'automargin': True},
                'xaxis': {'title': "Category", 'tickangle': -40, 'automargin': True}
            }
        },
        {
            'data': [
                Bar (x=words,
                    y=count_proportions
                )
            ],
            'layout': {
                'title': 'Frequency of Top 10 Words <br> as Percentage',
                'yaxis': {'title': 'Occurrence<br>(Out of 100)', 'automargin': True},
                'xaxis': {'title': 'Top 10 Words', 'automargin': True}
            }
        }
    ]
    
    # Encode plotly graphs in JSON
    ids = ["figure-{}".format(i) for i, _ in enumerate(figures)]
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Render web page with plotly figures
    return render_template('master.html', ids=ids, figuresJSON=figuresJSON, data_set=df)

# web page that handles user query and displays model results
@app.route('/go')

def go():

    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template('go.html',
                            query=query,
                            classification_result=classification_results
                          )


def main():
    app.run(host='0.0.0.0', port=3000, debug=True)


if __name__ == '__main__':
    main()
