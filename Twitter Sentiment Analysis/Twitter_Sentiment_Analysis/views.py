"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import jsonify, render_template, request
from Twitter_Sentiment_Analysis import app
import tensorflow as tf
from keras.preprocessing.text import Tokenizer, tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
import json
import pickle
from Twitter_Sentiment_Analysis.ll_queue import Queue
import json

model_path = r'C:/Users/yoganand/source/repos/Twitter Sentiment Analysis/Twitter Sentiment Analysis/Twitter_Sentiment_Analysis/LSTM_model'
loaded_model = tf.keras.models.load_model(model_path)

inputHistory=Queue()

def predict_class(text):
    '''Function to predict sentiment class of the passed text'''
    sentiment_classes = ['Negative', 'Neutral', 'Positive']
    max_words = 5000
    max_len=50

    token = open(model_path+'/tokenizer.pickle', 'rb')
    tokenizer=pickle.load(token)
    
    # Transforms text to a sequence of integers using a tokenizer object
    print(tokenizer)
    xt = tokenizer.texts_to_sequences(text)
    print(xt)
    # Pad sequences to the same length
    xt = pad_sequences(xt, padding='post', maxlen=max_len)
    # Do the prediction using the loaded model
    print(xt)
    yt = loaded_model.predict(xt).argmax(axis=1)
    # Print the predicted sentiment
    print('The predicted sentiment is', sentiment_classes[yt[0]])
    return sentiment_classes[yt[0]]
    

def addToHistory(newObject):
    while inputHistory.size>9:
        inputHistory.dequeue()
    inputHistory.enqueue(newObject)
    

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/tryNow', methods=['GET', 'POST'])
def tryNow():
    """Renders the tryNow page."""
    output=''
    if request.method == 'POST':
        inputText= request.form['inputText']
        #output=predict_class(inputText)
        output=predict_class([inputText])
        addToHistory({'input':inputText,'prediction':output})
        queue_dict = inputHistory.to_dict()
        result=f'The predicted sentiment is: {output}'
        #return jsonify(result=result)
        response = {
            'result': output,
            'inputHistory': json.dumps(queue_dict)
        }
        return jsonify(response)

    return render_template(
        'tryNow.html',
        title='Try Now',
        result=output,
        year=datetime.now().year,
        message='Your tryNow page.'
    )

@app.route('/dataSet')
def dataSet():
    """Renders the Data Set page."""
    return render_template(
        'dataSet.html',
        title='Data Sets',
        year=datetime.now().year,
        message='Data Set description page.'
    )

@app.route('/visualisations')
def visualisations():
    """Renders the visualisations page."""
    return render_template(
        'visualisations.html',
        title='Visualisations',
        year=datetime.now().year,
        message='Your contvisualisationsact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
