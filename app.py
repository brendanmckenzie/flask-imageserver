from flask import Flask
from imageserver import init_imageserver
import os

app = Flask(__name__)

init_imageserver(app, root_path=os.getenv('MEDIA_ROOT'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')

