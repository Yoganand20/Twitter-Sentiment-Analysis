"""
This script runs the Twitter_Sentiment_Analysis application using a development server.
"""

from os import environ
from Twitter_Sentiment_Analysis import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
